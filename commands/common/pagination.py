import discord


class Pagination(discord.ui.View):
    def __init__(self, interaction, page_getter, total_pages):
        self.interaction = interaction
        self.page_getter = page_getter
        self.total_pages = total_pages
        self.page = 1
        super().__init__(timeout=100)

    async def get_page(self):
        emb = await self.page_getter(self.page)
        emb.set_footer(text=f"Page {self.page}/{self.total_pages}")
        return emb

    async def view(self):
        emb = await self.get_page()
        if self.total_pages == 1:
            await self.interaction.response.send_message(embed=emb)
        elif self.total_pages > 1:
            self.update_buttons()
            await self.interaction.response.send_message(embed=emb, view=self)

    async def edit_page(self, interaction):
        emb = await self.get_page()
        self.update_buttons()
        await interaction.response.edit_message(embed=emb, view=self)

    def update_buttons(self):
        self.children[0].disabled = self.page == 1
        self.children[1].disabled = self.page == self.total_pages

    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction, button):
        self.page -= 1
        await self.edit_page(interaction)

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.blurple)
    async def next(self, interaction, button):
        self.page += 1
        await self.edit_page(interaction)

    async def on_timeout(self):
        message = await self.interaction.original_response()
        await message.edit(view=None)
