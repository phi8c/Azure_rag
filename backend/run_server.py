
import os
import multiprocessing

import uvicorn

from app.main import app


def main():
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "18080"))

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True,
        workers=1,
    )


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
