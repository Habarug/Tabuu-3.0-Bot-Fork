import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands

import utils.check
import utils.search
from utils.ids import GuildIDs
from views.macro import MacroButton


class Macros(commands.Cog):
    """Contains the logic of adding/removing macros.
    As well as listening for them.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        # Listens for the macros.
        async with aiosqlite.connect("./db/database.db") as db:
            macro_names = await db.execute_fetchall("""SELECT name FROM macros""")

            for name in macro_names:
                # It returns tuples, so we need the first (and only) entry
                name = name[0]
                if (
                    len(message.content.split()) == 1
                    and message.content == (f"{self.bot.main_prefix}{name}")
                    or message.content.startswith(f"{self.bot.main_prefix}{name} ")
                ):
                    matching_macro = await db.execute_fetchall(
                        """SELECT payload FROM macros WHERE name = :name""",
                        {"name": name},
                    )
                    payload = matching_macro[0][0]
                    await message.channel.send(payload)

                    await db.execute(
                        """UPDATE macros SET uses = uses + 1 WHERE name = :name""",
                        {"name": name},
                    )
                    await db.commit()

    @commands.hybrid_command()
    @app_commands.guilds(*GuildIDs.ADMIN_GUILDS)
    @app_commands.default_permissions(administrator=True)
    @utils.check.is_moderator()
    async def createmacro(self, ctx: commands.Context) -> None:
        """Creates a new macro with the desired name and payload."""
        view = MacroButton(ctx.author)

        await ctx.send(view=view)

    @commands.hybrid_command()
    @app_commands.guilds(*GuildIDs.ADMIN_GUILDS)
    @app_commands.describe(name="The name of the macro.")
    @app_commands.default_permissions(administrator=True)
    @utils.check.is_moderator()
    async def deletemacro(self, ctx: commands.Context, name: str) -> None:
        """Deletes a macro with the specified name."""
        async with aiosqlite.connect("./db/database.db") as db:
            macro_names = await db.execute_fetchall(
                """SELECT * FROM macros WHERE name = :name""", {"name": name}
            )

            # If the macro does not exist we want some kind of error message for the user.
            if len(macro_names) == 0:
                await ctx.send(f"The macro `{name}` was not found. Please try again.")
                return

            await db.execute(
                """DELETE FROM macros WHERE name = :name""", {"name": name}
            )

            await db.commit()

        await ctx.send(f"Deleted macro `{name}`")

    @deletemacro.autocomplete("name")
    async def deletemacro_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice]:
        async with aiosqlite.connect("./db/database.db") as db:
            macros = await db.execute_fetchall("""SELECT name FROM macros""")

        return utils.search.autocomplete_choices(current, [m[0] for m in macros])

    @commands.hybrid_command(aliases=["macros", "listmacros", "macrostats"])
    @app_commands.guilds(*GuildIDs.ALL_GUILDS)
    @app_commands.describe(macro="The macro you want to see the stats of.")
    async def macro(self, ctx: commands.Context, *, macro: str = None) -> None:
        """Gives you detailed information about a macro, or lists every macro saved."""
        if macro is None:
            async with aiosqlite.connect("./db/database.db") as db:
                macro_list = await db.execute_fetchall("""SELECT name FROM macros""")

            # It returns a list of tuples, so we need to extract them.
            macro_names = [m[0] for m in macro_list]
            await ctx.send(
                "The registered macros are:\n"
                f"`{self.bot.main_prefix}{f', {self.bot.main_prefix}'.join(macro_names)}`"
            )
            return

        async with aiosqlite.connect("./db/database.db") as db:
            matching_macro = await db.execute_fetchall(
                """SELECT * FROM macros WHERE name = :name""", {"name": macro}
            )

        # If the macro does not exist we want some kind of error message for the user.
        if len(matching_macro) == 0:
            await ctx.send(
                f"I could not find this macro. List all macros with `{self.bot.main_prefix}macros`."
            )
            return

        name, payload, uses, author_id = matching_macro[0]

        embed = discord.Embed(
            title="Macro info",
            color=self.bot.colour,
            description=f"**Name:** {self.bot.main_prefix}{name}\n**Uses:** {uses}\n"
            f"**Author:**<@{author_id}>\n**Output:**\n{payload}\n",
        )

        await ctx.send(embed=embed)

    @macro.autocomplete("macro")
    async def macro_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice]:
        async with aiosqlite.connect("./db/database.db") as db:
            macros = await db.execute_fetchall("""SELECT name FROM macros""")

        return utils.search.autocomplete_choices(current, [m[0] for m in macros])

    @createmacro.error
    async def createmacro_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(
            error, (commands.ExpectedClosingQuoteError, commands.UnexpectedQuoteError)
        ):
            await ctx.send(
                "Please do not create a macro with the `\"` letter. Use `'` instead."
            )


async def setup(bot) -> None:
    await bot.add_cog(Macros(bot))
    print("Macros cog loaded")
