import asyncio

from db import *
from interactions import (
    Attachment,
    AutocompleteContext,
    BaseContext,
    Button,
    ButtonStyle,
    Client,
    Color,
    ContextMenuContext,
    Embed,
    EmbedAuthor,
    EmbedField,
    Intents,
    Member,
    OptionType,
    Permissions,
    SlashCommandChoice,
    SlashCommandOption,
    SlashContext,
    StringSelectMenu,
    Timestamp,
    User,
    check,
    is_owner,
    listen,
    slash_command,
    slash_default_member_permission,
    slash_option,
    user_context_menu,
)

bot = Client(intents=Intents.DEFAULT)
db = DatabaseService()


def get_award_choices(query):
    return [{
        "name": opt.name,
        "value": str(opt.id)
    } for opt in db.award_list()]


# intents are what events we want to receive from discord, `DEFAULT` is usually fine


@listen(
)  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@slash_command(name="versao", description="Adicionar nova versão do modpack!")
@slash_default_member_permission(permission=Permissions.ADMINISTRATOR)
@slash_option(
    name="file",
    description=
    "Arquivo .zip da pasta .minecraft do modpack (não é só da pasta mods bell!!!)",
    required=True,
    opt_type=OptionType.ATTACHMENT,
)
async def add_versao(ctx: SlashContext, file: Attachment):
    await ctx.defer(ephemeral=True)

    version = db.version_add(file.url)
    version.save()
    await ctx.send("Versão adicionada.")


@slash_command(name="add_release",
               description="Adicionar nova versão do launcher!")
@slash_default_member_permission(permission=Permissions.ADMINISTRATOR)
@slash_option(
    name="file",
    description="Arquivo .zip da versão do launcher",
    required=True,
    opt_type=OptionType.ATTACHMENT,
)
@slash_option(
    name="versao",
    description="Número/nome da release",
    required=True,
    opt_type=OptionType.STRING,
)
async def add_release(ctx: SlashContext, file: Attachment, versao: str):
    await ctx.defer(ephemeral=True)

    inst = db.release_add(file.url, versao)
    inst.save()

    await ctx.send("Atualização adicionada.")


@slash_command(name="updater", description="Atualizar updater")
@slash_default_member_permission(permission=Permissions.ADMINISTRATOR)
@slash_option(
    name="file",
    description="Arquivo do updater",
    required=True,
    opt_type=OptionType.ATTACHMENT,
)
async def refresh_updater(ctx: SlashContext, file: Attachment):
    await ctx.defer(ephemeral=True)
    r = requests.get(file.url)
    path = os.path.join("releases", "update.exe")
    f = open(path, "wb")
    f.write(r.content)
    await ctx.send("Atualizador atualizado com sucesso . . .")


@slash_command(name="conquista",
               description="Adicionar conquista a um jogador!")
@slash_default_member_permission(permission=Permissions.ADMINISTRATOR)
@slash_option(
    name="operation",
    description="Operação",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Adicionar conquista", value="add"),
        SlashCommandChoice(name="Remover conquista", value="remove"),
    ],
)
@slash_option(
    name="user",
    description="Usuário associado ao jogador",
    required=True,
    opt_type=OptionType.USER,
)
@slash_option(
    name="award_id",
    description="Conquista a ser adicionada",
    required=True,
    opt_type=OptionType.STRING,
    autocomplete=True,
)
async def add_conquista(ctx: SlashContext, operation: str, user: User,
                        award_id: Award):
    # need to defer it, otherwise, it fails
    await ctx.defer(ephemeral=True)
    player = db.id_to_player(user.id.__str__())
    if player:
        try:
            if operation == "add":
                db.player_add_award_id(player, award_id)
            else:
                db.player_remove_award_id(player, award_id)
            await ctx.send("Operação concluida.")
        except Exception as e:
            await ctx.send(str(e))
    else:
        await ctx.send("Jogador não cadastrado.")


@slash_command(name="nova_conquista",
               description="Cadastrar uma nova conquista")
@slash_default_member_permission(permission=Permissions.ADMINISTRATOR)
@slash_option(
    name="name",
    description="Nome da conquista",
    required=True,
    opt_type=OptionType.STRING,
)
@slash_option(
    name="description",
    description="Descrição da conquista",
    required=True,
    opt_type=OptionType.STRING,
)
@slash_option(
    name="rarity",
    description="Raridade da conquista",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Secreta", value=AwardRarity.SECRET),
        SlashCommandChoice(name="Épica", value=AwardRarity.EPIC),
        SlashCommandChoice(name="Rara", value=AwardRarity.RARE),
        SlashCommandChoice(name="Comum", value=AwardRarity.COMMON),
        SlashCommandChoice(name="Ruim", value=AwardRarity.BAD),
    ],
)
@slash_option(
    name="icon",
    description="Imagem da conquista (transparente)",
    required=True,
    opt_type=OptionType.ATTACHMENT,
)
async def nova_conquista(
    ctx: SlashContext,
    name: str,
    description: str,
    rarity: AwardRarity,
    icon: Attachment,
):
    await ctx.defer(ephemeral=True)

    if not icon.content_type.startswith("image"):
        await ctx.send("Icone deve ser uma imagem válida!")
        return

    aw = db.award_new(icon_url=icon.proxy_url,
                      name=name,
                      description=description,
                      rarity=rarity)
    aw.save()

    await ctx.send("Conquista adicionada com sucesso.")


@slash_command(
    name="jornal",
    description="Atualizar jornal do servidor!",
    options=[
        SlashCommandOption(
            name=f"page{x}",
            description=f"Página {x} do jornal",
            required=False,
            type=OptionType.ATTACHMENT,
        ) for x in range(8)
    ],
)
@slash_default_member_permission(permission=Permissions.ADMINISTRATOR)
async def atualizar_jornal(ctx: SlashContext, *pages: Attachment):
    await ctx.defer(ephemeral=True)

    urls = []
    for page in pages:
        if not page:
            return

        if not page.content_type.startswith("image"):
            await ctx.send("Icone deve ser uma imagem válida!")
            return

        urls.append(page.proxy_url)

    if len(urls) == 0:
        await ctx.send("Não dá pra criar um jornal sem imagens!")
        return
    else:
        news = db.news_add(urls)
        db.update_server_info(news=news)
        await ctx.send("Jornal atualizado!")


@slash_command(name="eventos", description="Atualizar eventos no launcher!")
@slash_option(
    name="eventos",
    description="Lista de eventos separadas com uma barra '/'",
    required=True,
    opt_type=OptionType.STRING,
)
async def atualizar_eventos(ctx: SlashContext, eventos: str):
    await ctx.defer(ephemeral=True)

    events = eventos.split("/")

    db.update_server_info(events=events)

    await ctx.send(
        f"Eventos atualizados para: {', '.join('**' + ev + '**' for ev in events)}"
    )


@slash_command(name="pontos",
               description="Adicionar/subtrair pontos a um jogador!")
@slash_default_member_permission(permission=Permissions.ADMINISTRATOR)
@slash_option(
    name="user",
    description="Usuário associado ao jogador",
    required=True,
    opt_type=OptionType.USER,
)
@slash_option(
    name="operation",
    description="Operação",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Adicionar pontos", value="add"),
        SlashCommandChoice(name="Subtrair pontos", value="remove"),
    ],
)
@slash_option(
    name="points",
    description="Quantidade de pontos",
    required=True,
    opt_type=OptionType.INTEGER,
)
async def update_pontos(ctx: SlashContext, user: User, operation: str,
                        points: int) -> None:
    await ctx.defer(ephemeral=True)
    player = db.id_to_player(user.id.__str__())
    if player:
        signal = 1 if operation == "add" else -1
        points_ = points * signal
        result = player.score + points_
        if result >= 0:
            db.player_add_points(player, points_)
            await ctx.send("Pontuação atualizada.")
        else:
            await ctx.send(
                "Pontuação do jogador não pode ficar menor que zero!")
    else:
        await ctx.send("Jogador não cadastrado.")


@add_conquista.autocomplete("award_id")
async def autocomplete(ctx: AutocompleteContext):
    string_option_input = ctx.input_text
    await ctx.send(choices=get_award_choices(string_option_input))


@user_context_menu(name="Ver perfil do jogador!",
                   default_member_permissions=Permissions.ADMINISTRATOR)
async def user_profile(ctx: ContextMenuContext):
    await ctx.defer(ephemeral=True)
    member: Member = ctx.target
    await get_user_profile(ctx, member)


@slash_command(name="perfil", description="Ver perfil do usuário!")
@slash_option(
    name="user",
    description="Usuário associado ao jogador",
    required=True,
    opt_type=OptionType.USER,
)
async def user_profile_slash(ctx: SlashContext, user: User):
    await ctx.defer(ephemeral=True)
    await get_user_profile(ctx, user)


async def get_user_profile(ctx: BaseContext, user: User):
    player = db.id_to_player(user.id.__str__())
    if player:
        awards = player.awards
        awards_repr = ("".join(
            aw.discord_repr() + "\n"
            for aw in awards) if len(awards) > 0 else "Sem conquistas!")
        await ctx.send(embed=Embed(
            color=Color((255, 255, 255)),
            timestamp=Timestamp.now(),
            fields=[
                EmbedField(
                    "**Discord**", f"<@{user.id.__str__()}>", inline=True),
                EmbedField("**Nickname**", player.nickname, inline=True),
                EmbedField("**Pontos**", player.score.__str__(), inline=True),
                EmbedField(
                    "**Conquistas**",
                    awards_repr,
                    inline=False,
                ),
            ],
        ))


token_prod = ""
token_dev = ""


def start_bot():
    print("Iniciando bot!")
    bot.start(token_dev)


if __name__ == "__main__":
    start_bot()
