from pathlib import Path

import aiofiles


async def download_file(session, url, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    async with session.get(url) as response:
        if response.status != 200:
            return False

        async with aiofiles.open(output_path, "wb") as f:
            await f.write(await response.read())

    return True
