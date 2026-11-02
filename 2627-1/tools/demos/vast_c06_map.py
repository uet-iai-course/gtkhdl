MAP = Image.open(f"{FOLDER}/Vastopolis_Map.png")
print("Ảnh bản đồ:", MAP.size, "điểm ảnh, chế độ", MAP.mode)
MAP_SMALL = MAP.convert("RGB").resize((2600, 1322))      # thu nhỏ để vẽ nhanh

fig, ax = plt.subplots(figsize=(10, 5.1))
ax.imshow(MAP_SMALL); ax.axis("off")
ax.set_title("Vastopolis_Map.png: 13 khu vực, đường cao tốc, bệnh viện, sông")
plt.tight_layout()
plt.show()
