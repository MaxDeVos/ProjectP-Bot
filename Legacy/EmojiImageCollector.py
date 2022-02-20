# This works, it just needs to be dropped into main.py

# message: discord.Message
# prev: discord.Message
# async for message in self.channelDict["server-discussion"].history(limit=None):
#     if message.author.bot and message.content.__contains__("Understood. Sending"):
#         try:
#             async for prev in self.channelDict["server-discussion"].history(limit=10, before=message.created_at):
#                 if prev.content.__contains__("!emoji"):
#                     name = prev.content.split(" ")[1]
#                     async with aiohttp.ClientSession() as session:
#                         async with session.get(prev.attachments[0].url) as resp:
#                             if resp.status != 200:
#                                 print(getTimeStamp(), "[ERROR] Couldn't download file")
#                             data = io.BytesIO(await resp.read())
#                             with open(f"og_images/{name}_{prev.created_at.timestamp()}.jpg", "wb") as f:
#                                 f.write(data.getbuffer())
#                             f.close()
#         except:
#             pass
# print("DONE DOWNLOADING IMAGES")
# # print(data)
# # image = PIL.Image.open(io.BytesIO(data))
# # image.save(name+".jpg")