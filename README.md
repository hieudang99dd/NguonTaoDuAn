# C3D Tool Standard v1.1 — HDV

![Logo HDV](assets/HDV_LOGO_256.png)

**HDV — Civil 3D Tool Development Standard**  
**Cập nhật 26/10/2026:** bổ sung logo HDV chính thức làm thành phần nhận diện bắt buộc của quy trình thiết kế, UI, Ribbon, installer và tài liệu; không thay đổi thuật toán đã chốt.

## Hồ sơ

- `QUY_TRINH_CHUAN_TOOL_CIVIL3D.md` — đặc tả đầy đủ từ phân tích ZIP đến build/NETLOAD/installer, đã bổ sung mục **4.1 logo HDV**.
- `QUY_TRINH_CO_LOGO.html` — bản đọc trực quan phong cách đen/cam, xem offline sau khi giải nén ZIP.
- `HUONG_DAN_SU_DUNG_LOGO_HDV.md` — vị trí, kích thước, quy định, triển khai và QA logo.
- `QA_CHECKLIST.md` — có thêm kiểm tra logo trên UI, Ribbon/installer thực tế.
- `assets/` — logo gốc và biến thể PNG/ICO đủ cho tài liệu/UI/bộ cài.
- `templates/branding.json` — ví dụ quy định logo (không phải schema runtime đã tích hợp).
- `templates/tool.json` — ví dụ metadata Ribbon gốc, giữ nguyên để không làm hỏng updater hiện hành.
- `templates/PROJECT_STATUS.md` — biểu mẫu trạng thái kỹ thuật và trạng thái logo.
- `SHA256SUMS.txt` — checksum các file trong gói, phục vụ kiểm tra toàn vẹn.

## Phạm vi hoàn thành

Bộ này là **tài liệu + hình ảnh + template**, không phải phiên bản mới của DLL SLB/QSL/Solid Cutter hoặc installer. Trong mã nguồn từng tool, việc nhúng logo vào WebView2, CUIX/Ribbon và icon của EXE là bước **triển khai phải làm và test trên Windows/Civil 3D**; không tuyên bố đã thực hiện trong bộ chuẩn này.

**Nguồn kiểm toán:** xem mục 0 trong SOP; ZIP của một số tool bản mới nhất chưa thể đọc byte tại lần tổng hợp v1.0.
