from ftplib import FTP

from loguru import logger

from config import FTP_SERVERS


@logger.catch
def send_file_to_server(file_name: str, file_path: str, server: dict) -> None:
    try:
        ftp = FTP(host=server["host"])
        ftp.login(user=server["user"], passwd=server["passwd"])
        ftp.cwd(server["base_path"])
        with open(file_path, "rb") as file:
            ftp.storbinary("STOR " + file_name, file)
        ftp.quit()
        logger.info(f"Send File To Server Success: {file_name} -> {server['host']}")
    except Exception as e:
        logger.error(
            f"Send File To Server Error ({file_name} -> {server['host']}): {e}"
        )


@logger.catch
def send_file_to_servers(file_path: str) -> None:
    file_name = file_path.replace("base/", "")
    for server in FTP_SERVERS:
        send_file_to_server(file_name=file_name, file_path=file_path, server=server)
