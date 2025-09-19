import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

# 🔐 Token laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 🎯 Gezielte Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# 🤖 Bot-Setup
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# 📁 Musikverzeichnis & Steuerung
MUSIC_DIR = "music"
playlist = []
current_index = -1
autoplay_enabled = True

# 🚀 Bot ist bereit
@bot.event
async def on_ready():
    print(f"🎵 Bot ist online als {bot.user}")

# 🔁 Wrapper für asynchrone Wiedergabe
def play_next_track_wrapper(ctx):
    async def inner():
        await play_next_track(ctx)
    bot.loop.create_task(inner())

# ▶️ Nächsten Track abspielen
async def play_next_track(ctx):
    global playlist, current_index, autoplay_enabled
    vc = ctx.voice_client
    if not vc or not vc.is_connected() or not playlist or not autoplay_enabled:
        return

    current_index = (current_index + 1) % len(playlist)
    filepath = os.path.join(MUSIC_DIR, playlist[current_index])
    source = discord.FFmpegPCMAudio(filepath, options="-filter:a volume=1.0")
    vc.play(source, after=lambda e: play_next_track_wrapper(ctx))

    embed = discord.Embed(
        title="▶️ Nächster Track",
        description=playlist[current_index],
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# 🔀 Shuffle starten
async def start_shuffle(ctx):
    global playlist, current_index, autoplay_enabled
    vc = ctx.voice_client
    if not vc or not vc.is_connected():
        await ctx.send("❌ Bot ist nicht im Sprachkanal.")
        return

    autoplay_enabled = True
    playlist = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]
    if not playlist:
        await ctx.send("📁 Keine Musikdateien vorhanden.")
        return

    random.shuffle(playlist)
    current_index = 0
    filepath = os.path.join(MUSIC_DIR, playlist[current_index])
    source = discord.FFmpegPCMAudio(filepath, options="-filter:a volume=1.0")
    vc.play(source, after=lambda e: play_next_track_wrapper(ctx))

    embed = discord.Embed(
        title="🔀 Shuffle gestartet",
        description=playlist[current_index],
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# 📡 Sprachkanal beitreten
@bot.command()
async def join(ctx):
    member = ctx.author
    if member.voice and member.voice.channel:
        channel = member.voice.channel
        if not ctx.voice_client:
            await channel.connect()
        await ctx.send(f"✅ Verbunden mit {channel.name}")
        await start_shuffle(ctx)
    else:
        await ctx.send("❌ Du bist in keinem Sprachkanal.")

# 👋 Sprachkanal verlassen
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Bot hat den Sprachkanal verlassen.")
    else:
        await ctx.send("❌ Bot ist nicht verbunden.")

# 📃 Liste der Musikdateien
@bot.command()
async def list(ctx):
    files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]
    if not files:
        await ctx.send("📁 Keine Musikdateien gefunden.")
    else:
        msg = "\n".join(f"{i+1}. {f}" for i, f in enumerate(files))
        await ctx.send(f"🎶 Verfügbare Tracks:\n{msg}")

# ▶️ Musik abspielen
@bot.command()
async def play(ctx, filename=None):
    global playlist, current_index, autoplay_enabled
    vc = ctx.voice_client
    if not vc or not vc.is_connected():
        await ctx.send("❌ Bot ist nicht im Sprachkanal. Nutze zuerst !join.")
        return

    autoplay_enabled = True
    if filename:
        filepath = os.path.join(MUSIC_DIR, filename)
        if not os.path.isfile(filepath):
            await ctx.send("❌ Datei nicht gefunden.")
            return
        playlist = [filename]
        current_index = 0
    else:
        playlist = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]
        if not playlist:
            await ctx.send("📁 Keine Musikdateien vorhanden.")
            return
        current_index = random.randint(0, len(playlist) - 1)

    filepath = os.path.join(MUSIC_DIR, playlist[current_index])
    source = discord.FFmpegPCMAudio(filepath, options="-filter:a volume=1.0")
    vc.play(source, after=lambda e: play_next_track_wrapper(ctx))

    embed = discord.Embed(
        title="▶️ Spiele",
        description=playlist[current_index],
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

# ⏭️ Nächsten Track manuell starten
@bot.command()
async def next(ctx):
    global autoplay_enabled
    vc = ctx.voice_client
    if not vc or not vc.is_connected():
        await ctx.send("❌ Bot ist nicht im Sprachkanal.")
        return

    autoplay_enabled = True
    vc.stop()
    await ctx.send("⏭️ Nächster Track wird gespielt.")

# ⏹️ Wiedergabe stoppen und Autoplay deaktivieren
@bot.command()
async def stop(ctx):
    global autoplay_enabled
    vc = ctx.voice_client
    if vc and vc.is_playing():
        autoplay_enabled = False
        vc.stop()
        await ctx.send("⏹️ Wiedergabe gestoppt und Autoplay deaktiviert.")
    else:
        await ctx.send("❌ Keine Wiedergabe aktiv.")

# ⏸️ Wiedergabe pausieren
@bot.command()
async def pause(ctx):
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await ctx.send("⏸️ Wiedergabe pausiert.")
    else:
        await ctx.send("❌ Keine Wiedergabe aktiv.")

# ▶️ Wiedergabe fortsetzen
@bot.command()
async def resume(ctx):
    vc = ctx.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send("▶️ Wiedergabe fortgesetzt.")
    else:
        await ctx.send("❌ Nichts zum Fortsetzen.")

# ℹ️ Hilfe anzeigen
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🎵 Musikbot Befehle",
        color=discord.Color.purple()
    )
    embed.add_field(name="!join", value="Bot tritt deinem Sprachkanal bei und startet Shuffle", inline=False)
    embed.add_field(name="!leave", value="Bot verlässt den Sprachkanal", inline=False)
    embed.add_field(name="!list", value="Zeigt alle verfügbaren MP3-Dateien", inline=False)
    embed.add_field(name="!play [Dateiname]", value="Spielt eine bestimmte Datei oder zufällig", inline=False)
    embed.add_field(name="!next", value="Spielt den nächsten Track", inline=False)
    embed.add_field(name="!shuffle", value="Mischt die Playlist und startet Wiedergabe", inline=False)
    embed.add_field(name="!pause", value="Pausiert die Wiedergabe", inline=False)
    embed.add_field(name="!resume", value="Setzt die Wiedergabe fort", inline=False)
    embed.add_field(name="!stop", value="Stoppt die Wiedergabe und deaktiviert Autoplay", inline=False)
    await ctx.send(embed=embed)

# 🚀 Bot starten
bot.run(TOKEN)