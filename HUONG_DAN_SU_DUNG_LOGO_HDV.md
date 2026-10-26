# HƯỚNG DẪN TÍCH HỢP LOGO HDV — CIVIL 3D TOOLS

![Logo HDV](assets/HDV_LOGO_256.png)

**Phiên bản quy chuẩn:** 1.1.0 — 26/10/2026  
**Logo chính thức:** hình HDV do người dùng gửi. Trong bộ này file gốc được sao chép nguyên trạng.

## 1. Vai trò

Logo HDV là dấu hiệu nhận diện thống nhất trên bộ tài liệu phát triển, giao diện WebView2/PaletteSet, Ribbon và các bộ cài HVDTools. Tên sản phẩm là **tên tiếng Anh đầy đủ** của từng tool; logo không thay thế tên sản phẩm. Giữ tên command riêng như `SLB` / `QSL` theo đặc tả từng tool.

## 2. Cấu trúc asset

- `assets/HDV_LOGO_ORIGINAL_2048.png` — logo gốc (không chỉnh sửa).
- `assets/HDV_LOGO_16.png`, `_32.png`, `_48.png`, `_64.png`, `_128.png`, `_256.png`, `_512.png` — thu nhỏ trung thực giữ nguyên tỷ lệ.
- `assets/HDV_TOOLS.ico` — tài nguyên ICO từ logo gốc, dành cho build installer Windows nếu toolchain hỗ trợ.

Không chỉnh màu nền, không xóa họa tiết, không cắt chữ hoặc co kéo méo tỷ lệ. Nếu Ribbon 16×16 khó nhận diện, phải duyệt icon tối giản riêng chứ không được tự ý thay đổi logo chuẩn.

## 3. Nơi hiển thị

### 3.1. PaletteSet / WebView2

Logo tối đa 40×40 CSS pixels đặt bên trái tên công cụ tiếng Anh đầy đủ. Khi dock hẹp, tên được xuống dòng hợp lý; logo không bị co giãn hoặc che các nút. Logo tiêu đề phải đọc được ngay ở 350 px. Tiêu đề chi tiết/thao tác bằng tiếng Việt ngắn gọn.

Ví dụ:

```html
<header class="tool-brand">
  <img src="assets/HDV_LOGO_64.png" alt="HDV" width="40" height="40">
  <div><strong>Solid Builder</strong><span>SLB · Civil 3D</span></div>
</header>
```

**Lưu ý:** ví dụ HTML chỉ là mẫu bố cục; `src` phải hợp với đường dẫn deploy hoặc embedded resource. Không đổi code CadHost khi chưa đọc cấu trúc host hiện có.

### 3.2. Ribbon

Bố trí các nhóm theo lĩnh vực (ví dụ **BIM TUYẾN**), mỗi tác vụ có nhãn và command rõ ràng. Hình HDV là nhận diện bộ sản phẩm; icon tác vụ cần phân biệt được chức năng. `tool.json` mẫu của HVDTools hiện có trường `ribbonIcon: "box"`; chưa có chứng cứ nó đọc đường dẫn PNG. Muốn dùng icon thật, phải kiểm tra/updater, implement parser/resource và test Civil 3D Windows, không chỉ thay text JSON.

### 3.3. Installer / Updater

`HDV_TOOLS.ico` có thể làm icon cho EXE sau khi build Windows và kiểm tra resource. Không tự xem việc có `.ico` trong ZIP là EXE đã được gắn logo hoặc ký số.

### 3.4. Hồ sơ, tài liệu, gói bàn giao

Logo xuất hiện trên SOP, README, checklist, mô phỏng quy trình. Asset dùng đường dẫn tương đối, có SHA256 và có mặt trong ZIP nguồn. ZIP CAD production chỉ kèm kích thước cần thiết (tránh lãng phí dung lượng).

## 4. Chống lỗi và nghiệm thu

1. Kiểm tra SHA256 logo trong ZIP so với logo gốc.
2. Kiểm tra hình ảnh đúng tỷ lệ và không méo ở UI rộng/hẹp, nhiều DPI.
3. Kiểm tra **logo + tên tiếng Anh đầy đủ**, không dùng chỉ nhãn command.
4. Kiểm tra Ribbon/installer **trên Windows/C3D thực**, ghi trạng thái NOT_RUN nếu chưa kiểm chứng.
5. Kiểm tra cấu trúc đường dẫn PNG/.ico sau deploy, cả với NETLOAD và autoload.

**Trạng thái tại lần cập nhật:** tài liệu, asset và preview đã bổ sung. Chưa sửa mã nguồn DLL/CadHost, chưa build lại installer, chưa tuyên bố logo thực đã hiển thị trên Ribbon hoặc EXE.
