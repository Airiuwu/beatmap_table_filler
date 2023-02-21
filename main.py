from objects import timerHelper, bcolors
import databases
import asyncio
import uvloop
import config
import os, re

async def main():
    t = timerHelper.Timer()
    database = databases.Database(config.url)
    error_amount = 0

    os.system("clear")
    async with database:
        for row in await database.fetch_all('SELECT * FROM `beatmaps` WHERE `file_name` IS NOT NULL ORDER BY `beatmaps`.`id` ASC'):
            t.start()
            try:
                song_details = re.split(r"^(?P<artist>.+) - (?P<title>.+) \((?P<creator>.+)\) \[(?P<version>.+)\]\.osu$", row['file_name'])

                await database.execute(
                'UPDATE beatmaps SET artist = :artist, creator = :creator, title = :title, version = :version WHERE id = :id', 
                values={"artist": song_details[1], "creator": song_details[3], "title": song_details[2], "version": song_details[4], "id": row['id']}
                )

                t.end()
                print(f"{bcolors.OKMSG}{row['id']} => Updated {row['file_name']} {bcolors.BLUE} ({t.time_str()}){bcolors.ENDC}")

            except IndexError:
                error_amount += 1
                pass

        print(f"Errors => {error_amount}")

uvloop.install()
asyncio.run(main())
