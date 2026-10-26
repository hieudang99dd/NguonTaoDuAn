# HƯỚNG DẪN LOGO HDV — GIAO DIỆN TOOL CIVIL 3D

![Logo HDV](assets/HDV_LOGO_256.png)

**Phiên bản:** 1.3.1 — 26/10/2026

## Vai trò
Logo HDV thống nhất trên giao diện PaletteSet/WebView2 và tài liệu kỹ thuật. Luôn đặt cạnh **tên tiếng Anh đầy đủ** của tool; mã lệnh CAD là nhãn riêng, ví dụ `SLB` hoặc `QSL`.

## Tài nguyên
- `assets/HDV_LOGO_ORIGINAL_2048.png` — ảnh gốc bảo toàn nguyên trạng và SHA256.
- `assets/HDV_LOGO_16.png`, `_32.png`, `_48.png`, `_64.png`, `_128.png`, `_256.png`, `_512.png` — các phiên bản thu nhỏ.
- Không thay màu, bóp méo, cắt xén hoặc thay chữ trong logo.

## Giao diện PaletteSet / WebView2
- Logo gợi ý 40×40 CSS px, dùng `object-fit:contain`, đặt bên trái tên tiếng Anh đầy đủ.
- Giao diện nền tối và nhấn cam, dock trái/phải, không che nút ở chiều rộng 350 px, kiểm tra DPI 100–200%.
- Nhúng asset vào resource hoặc chép cùng thư mục của DLL và cấu hình đường dẫn tương đối phù hợp.

Ví dụ:

```html
<header class="tool-brand">
  <img src="assets/HDV_LOGO_64.png" alt="HDV" width="40" height="40">
  <div><strong>Solid Builder</strong><span>SLB · Civil 3D</span></div>
</header>
```

## Tài liệu và bàn giao NETLOAD
Logo được dùng trên README, SOP và các trang mô phỏng. Với thư mục DLL nạp bằng `NETLOAD`, bảo đảm WebView2 truy cập được ảnh thực tế nếu không nhúng trực tiếp trong assembly. Giữ asset cần thiết và ghi nguồn/hàm băm khi bàn giao.

## Kiểm thử
1. Kiểm tra SHA256 asset nguồn.
2. Kiểm tra đúng tỷ lệ trên Palette và nhiều DPI.
3. Kiểm tra logo + tên tiếng Anh đầy đủ, không chỉ mã lệnh.
4. Nạp CadHost qua `NETLOAD`, gọi lệnh và kiểm tra logo trực tiếp trên Civil 3D; chưa kiểm chứng thì ghi `NOT_RUN`.

**Giới hạn:** tài liệu hướng dẫn không phải bằng chứng đã tích hợp logo trong một DLL cụ thể.
