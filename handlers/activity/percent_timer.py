from copy import copy

from config import HOURS_IN_WEEK, MILES_IN_HOUR
from handlers.activity.activity_functions import *
from handlers.activity.database import *
from texts.messages import LOADING


@logger.catch
def get_timing(timing_str):
    timing_arr = timing_str.split("\n")
    timing_dict = {}
    for timing in timing_arr:
        try:
            hour, percent = map(int, timing.split(" - "))
        except Exception as e:
            logger.warning(f"Get Timing Error: {e}")
            try:
                hour, percent = map(int, timing.split("-"))
            except Exception as e:
                logger.warning(f"Get Timing Error: {e}")
                try:
                    hour, percent = map(int, timing.split(" -"))
                except Exception as e:
                    logger.warning(f"Get Timing Error: {e}")
                    try:
                        hour, percent = map(int, timing.split("- "))
                    except Exception as e:
                        logger.warning(f"Get Timing Error: {e}")
                        return None
        timing_dict[hour] = percent
    if sum(timing_dict.values()) == 100:
        return timing_dict
    else:
        return None


@logger.catch
async def unsubscribe_timing(accounts, channel_link):
    if len(accounts) >= 6:
        week_percents = {
            1: math.ceil(len(accounts) * 0.1),
            2: math.ceil(len(accounts) * 0.08),
            3: math.ceil(len(accounts) * 0.05),
            4: math.ceil(len(accounts) * 0.03),
            5: math.ceil(len(accounts) * 0.02),
            6: math.ceil(len(accounts) * 0.02),
        }
        keys = []
        for week in range(6):
            for acc in range(week_percents[week + 1]):
                hour = week * HOURS_IN_WEEK + random.randint(1, HOURS_IN_WEEK)
                keys.append(hour)

        shuffle(accounts)

        link = channel_link

        if "https://t.me/+" in channel_link:
            link = channel_link.replace("https://t.me/+", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
        elif "https://t.me/joinchat/" in channel_link:
            link = channel_link.replace("https://t.me/joinchat/", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                channel_link = str(channel.title)
            except Exception as e:
                channel_link = str(channel.chat.title)
            link_checker.disconnect()
        elif "t.me/+" in channel_link:
            link = channel_link.replace("t.me/+", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()
        elif "t.me/joinchat/" in channel_link:
            link = channel_link.replace("t.me/joinchat/", "")
            link_checker = await connect_to_account((await get_list_of_numbers())[0])
            channel = await link_checker(
                functions.messages.CheckChatInviteRequest(link)
            )
            try:
                link = str(channel.title)
            except Exception as e:
                link = str(channel.chat.title)
            link_checker.disconnect()

        args = [link, 1, 1]

        account_iter = 0
        start = time.time()

        for time_iter in range(1, max(keys) + 1):
            if time_iter in keys:
                logger.info("Unsubscribe Timing: trying to unsubscribe")
                current_account = []
                try:
                    try:
                        current_account.append(accounts[account_iter])
                    except Exception as e:
                        logger.error(f"Unsubscribe Timing Error: {e}")

                    is_success = await leave_channel(
                        args=args,
                        accounts=current_account,
                        unsubscribe_percent_timing=True,
                    )
                    logger.info(f"Unsubscribe Timing Success: {is_success}")
                    account_iter += 1

                    if not is_success:
                        return False
                except Exception as e:
                    logger.error(f"Unsubscribe Timing Error: {e}")
            else:
                await asyncio.sleep(MILES_IN_HOUR)

            end = time.time()
            logger.info(f"Unsubscribe Timing: {start - end}")

        return True


@logger.catch
async def add_task_to_db(link, count, timing, is_sub):
    if is_sub == 1:
        accounts = await get_list_of_numbers(link=link, sub=True)
    elif is_sub == -1:
        accounts = await get_list_of_numbers(link=link, sub=False)
    else:
        accounts = await get_list_of_numbers()
    shuffle(accounts)
    accounts_for_timing = accounts[:count]
    task_id = add_task(accounts=accounts_for_timing, count=count, timing=timing)
    return task_id


@logger.catch
async def percent_timer(
    timing,
    function,
    args,
    prev_message: Message = None,
    return_accounts=False,
    is_sub=0,
):
    """
    :param is_sub: False = -1; True = 1.
    :param return_accounts: for unsubscribe timing
    :param prev_message:
    :param timing: get_timing()
    :param function: function of account's activity
    :param args: [channel_link, count],
                [channel_link, count, last_post_id, count_posts],
                [channel_link, count, post_id, position]
    :return: None
    """

    try:
        (
            message,
            count,
            link,
            task_id,
            keys,
            sum_current_count,
            last_account_iter,
            start,
        ) = await initialize_variables_for_timer(args, timing, is_sub, prev_message)

        accounts_to_return = []
        if return_accounts:
            accounts_to_return = get_phone_by_task(task_id)

        accounts = await timer_cycle(
            message,
            count,
            task_id,
            keys,
            sum_current_count,
            last_account_iter,
            start,
            timing,
            function,
            args,
            return_accounts,
        )

        delete_task(task_id)

        if return_accounts:
            return True, accounts_to_return
        return True

    except Exception as e:
        logger.error(f"Percent Timer Error: {e}")


@logger.catch
async def timer_cycle(
    message,
    count,
    task_id,
    keys,
    sum_current_count,
    last_account_iter,
    start,
    timing,
    function,
    args,
    return_accounts,
):
    for time_iter in range(1, max(keys) + 1):
        checked_status = await check_task_status(task_id)
        if not checked_status:
            break
        if time_iter in keys:
            is_success, last_account_iter = await timing_iteration(
                time_iter,
                timing,
                keys,
                count,
                sum_current_count,
                args,
                task_id,
                last_account_iter,
                function,
                message,
            )
            if not is_success:
                return timing_not_success_return(return_accounts, task_id)
        else:
            await asyncio.sleep(MILES_IN_HOUR)
        end = time.time()
        logger.info(f"Timer Cycle Timing: {start - end}")
    return return_accounts


@logger.catch
async def timing_iteration(
    time_iter,
    timing,
    keys,
    count,
    sum_current_count,
    args,
    task_id,
    last_account_iter,
    function,
    message,
):
    current_count, last_iter = get_current_count(
        time_iter, timing, keys, count, sum_current_count
    )
    if current_count != 0:
        try:
            current_args, loading_args, current_accounts = get_timing_args(
                current_count, args, task_id, last_account_iter, count
            )

            is_success = await function(
                args=current_args,
                accounts=current_accounts,
                last_iter=last_iter,
                prev_message=message,
                loading_args=loading_args,
                task_id=task_id,
            )

            last_account_iter += current_count
            return is_success, last_account_iter
        except Exception as e:
            logger.error(f"Timing Cycle Error: {e}")
    return True, last_account_iter


@logger.catch
def timing_not_success_return(return_accounts, task_id):
    if return_accounts:
        return False, get_phone_by_task(task_id)
    return False


@logger.catch
def get_timing_args(current_count, args, task_id, last_account_iter, count):
    delay = round(MILES_IN_HOUR / current_count)
    current_args = copy(args)
    current_args.append(delay)
    current_accounts = []
    try:
        current_accounts = get_phone_by_task(task_id)[:current_count]
    except Exception as e:
        logger.error(f"Get Timing Error: {e}")
    current_args[1] = current_count
    loading_args = [last_account_iter, count]
    return current_args, loading_args, current_accounts


@logger.catch
def get_current_count(time_iter, timing, keys, count, sum_current_count):
    last_iter = False
    hour = time_iter
    percent = timing[hour]
    if time_iter != max(keys):
        current_count = round(count * percent / 100)
        if current_count + sum_current_count <= count:
            sum_current_count += current_count
        else:
            current_count = count - sum_current_count
    else:
        last_iter = True
        current_count = count - sum_current_count
    return current_count, last_iter


@logger.catch
async def check_task_status(task_id):
    try:
        task_status = get_task_by_id(task_id)
        if task_status is not None and task_status != 200:
            task_status = task_status[2]
        else:
            logger.info("Task #" + str(task_id) + " was stopped")
            return False
        logger.info("#" + str(task_id) + "\tstatus:\t" + str(task_status))
        while task_status == 0:
            await asyncio.sleep(60)
            task_status = get_task_by_id(task_id)
            if task_status is not None and task_status != 200:
                task_status = task_status[2]
        if task_status is None or task_status == 200:
            logger.info("Task #" + str(task_id) + " was stopped")
            return False
        return True
    except Exception as e:
        logger.error(f"Check Task Status Error: {e}")
        return False


@logger.catch
async def initialize_variables_for_timer(args, timing, is_sub, prev_message):
    count = args[1]
    link = args[0]
    task_id = await add_task_to_db(link=link, count=count, timing=timing, is_sub=is_sub)

    await prev_message.answer(text="Задача #" + str(task_id))
    message = await prev_message.answer(text=LOADING[0])
    await prev_message.delete()

    keys = list(timing.keys())
    sum_current_count = 0
    last_account_iter = 0

    start = time.time()

    return (
        message,
        count,
        link,
        task_id,
        keys,
        sum_current_count,
        last_account_iter,
        start,
    )
