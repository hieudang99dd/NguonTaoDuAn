# Tệp dung lượng lớn

Do giới hạn kích thước dữ liệu trong kết nối GitHub, các tệp lớn được lưu thành nhiều phần **nhị phân** theo thứ tự; dữ liệu không bị mã hóa lại hoặc mất chất lượng.

Sau khi tải/cloning repository, chạy:

```bash
python scripts/restore_large_assets.py
```

Script sẽ ghép nguyên vẹn:

- `assets/HDV_LOGO_ORIGINAL_2048.png` — 5.433.767 bytes, SHA256 `1aae883214da4a2d23e7178c7a7f43983d683e23bad68681389c8d759a67b77a`.
- `release/C3D_TOOL_STANDARD_V1_2_HDV_ALGORITHM_INVENTORY.zip` — 6.006.135 bytes, SHA256 `99fa1c1bc6a9936991c754ebc7de813d63669fe0c0df6bd8efe80fcb1dbf6429`.
- `release/C3D_TOOL_STANDARD_V1_1_HDV_LOGO.zip` — 5.996.287 bytes, SHA256 `016653a79345db406bc4c942c01c14e721eea58d2e231854c51bcb4081acb983`.

Ảnh phục vụ hiển thị (`assets/HDV_LOGO_256.png`, `HDV_LOGO_512.png`, v.v.) và toàn bộ tài liệu, template có sẵn trực tiếp không cần chạy script.

*Lưu ý:* Đường dẫn `release/*.zip` ở repo là bản ghép sau khi chạy script; không có sẵn dưới dạng một tệp zip trên GitHub khi chưa ghép.
