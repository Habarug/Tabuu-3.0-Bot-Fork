import aiosqlite

import utils.logger


async def setup_db(filepath: str = "./db/database.db") -> None:
    """Sets up the database with the required tables.
    Only really needed for first-time setup, or when we add a table.
    """
    async with aiosqlite.connect(filepath) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS warnings(
                user_id INTEGER,
                warn_id INTEGER,
                mod_id INTEGER,
                reason TEXT,
                timestamp INTEGER)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS starboardmessages(
                original_id INTEGER,
                starboard_id INTEGER)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS reminder(
                user_id INTEGER,
                reminder_id INTEGER,
                channel_id INTEGER,
                date INTEGER,
                read_time TEXT,
                message TEXT)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS reactrole(
                message_id INTEGER,
                exclusive INTEGER,
                rolereq TEXT,
                emoji TEXT,
                role INTEGER)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS profile(
                user_id INTEGER,
                tag TEXT,
                region TEXT,
                mains TEXT,
                secondaries TEXT,
                pockets TEXT,
                note TEXT,
                colour INTEGER)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS muted(
                user_id INTEGER,
                muted INTEGER)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS macros(
                name TEXT,
                payload TEXT,
                uses INTEGER,
                author INTEGER)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS userbadges(
                user_id INTEGER,
                badges TEXT)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS badgeinfo(
                badge TEXT,
                info TEXT)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS usernames(
                user_id INTEGER,
                old_name TEXT,
                timestamp INTEGER)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS nicknames(
                user_id INTEGER,
                old_name TEXT,
                guild_id INTEGER,
                timestamp INTEGER)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS notes(
                note_id INTEGER,
                user_id INTEGER,
                timestamp INTEGER,
                mod_id INTEGER,
                note TEXT)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS trueskill(
                user_id INTEGER,
                rating REAL,
                deviation REAL,
                wins INTEGER,
                losses INTEGER,
                matches TEXT)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS matches(
                match_id INTEGER,
                winner_id INTEGER,
                loser_id INTEGER,
                timestamp INTEGER,
                old_winner_rating REAL,
                old_winner_deviation REAL,
                old_loser_rating REAL,
                old_loser_deviation REAL,
                new_winner_rating REAL,
                new_winner_deviation REAL,
                new_loser_rating REAL,
                new_loser_deviation REAL)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS level(
                id INTEGER,
                level INTEGER,
                xp INTEGER,
                messages INTEGER)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS commands(
                command TEXT,
                uses INTEGER,
                last_used INTEGER)"""
        )

        await db.commit()

        logger = utils.logger.get_logger("bot.db")
        logger.info("Database setup complete!")


async def setup_ufd(filepath: str = "./db/ultimateframedata.db") -> None:
    """Sets up the UFD database with the required tables.
    You will need to populate the tables with the data from the UFD website yourself.
    Check out https://www.github.com/atomflunder/ultimateframedata-scraping for details.
    You will need to do some manual cleanup though.
    Only really needed for first-time setup.
    """
    async with aiosqlite.connect(filepath) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS moves(
                character TEXT,
                input TEXT,
                move_name TEXT,
                special_hitbox TEXT,
                full_move_name TEXT,
                frame_startup TEXT,
                frame_active TEXT,
                frame_endlag TEXT,
                frame_onshield TEXT,
                frame_shieldlag TEXT,
                frame_shieldstun TEXT,
                frame_total TEXT,
                autocancels TEXT,
                actionable_before_landing TEXT,
                damage TEXT,
                hitbox_gif TEXT,
                notes TEXT)"""
        )

        await db.execute(
            """CREATE TABLE IF NOT EXISTS stats(
                character TEXT,
                image TEXT,
                weight TEXT,
                gravity TEXT,
                walk_speed TEXT,
                run_speed TEXT,
                initial_dash TEXT,
                air_speed TEXT,
                total_air_acceleration TEXT,
                sh_fh_shff_fhff_frames TEXT,
                fall_speed_fast_fall_speed TEXT,
                oos1 TEXT,
                oos2 TEXT,
                oos3 TEXT,
                shield_grab TEXT,
                shield_drop TEXT,
                jump_squat TEXT)"""
        )
