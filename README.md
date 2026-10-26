# C3D Tool Standard v1.3 — HDV

![Logo HDV](assets/HDV_LOGO_256.png)

**HDV — Civil 3D Tool Development Standard**  
**Cập nhật 26/10/2026:** phạm vi hiện hành là phát triển, biên dịch DLL CadHost và nghiệm thu trực tiếp bằng `NETLOAD`.

## Hồ sơ

- `QUY_TRINH_CHUAN_TOOL_CIVIL3D.md` — quy trình tạo, build và nghiệm thu DLL NETLOAD.
- `QUY_TRINH_CO_LOGO.html` — bản đọc trực quan phong cách đen/cam, xem offline sau khi giải nén ZIP.
- `HUONG_DAN_SU_DUNG_LOGO_HDV.md` — vị trí, kích thước, quy định, triển khai và QA logo.
- `QA_CHECKLIST.md` — checklist build, NETLOAD, UI và nghiệm thu nghiệp vụ DWG.
- `assets/` — logo chuẩn cho PaletteSet, WebView2 và tài liệu.
- `templates/branding.json` — mẫu cấu hình logo cho UI và tài liệu.
- `templates/tool.json` — metadata tên, phiên bản, lệnh và DLL CadHost.
- `templates/PROJECT_STATUS.md` — biểu mẫu trạng thái kỹ thuật và trạng thái logo.
- `SHA256SUMS.txt` — checksum các file trong gói, phục vụ kiểm tra toàn vẹn.

## Phạm vi hoàn thành

Bộ repository hiện tại là **tài liệu + hình ảnh + template**, không phải DLL đã build của các tool. Chuẩn bàn giao sản phẩm từ các dự án tool là **DLL CadHost nạp bằng `NETLOAD` + dependencies/UI cần thiết + full source và báo cáo QA**. 

**Nguyên tắc:** mọi dự án sử dụng bộ chuẩn phải tự kiểm toán mã nguồn và bằng chứng nghiệm thu của chính mình.

## Lấy đủ ảnh gốc và ZIP bàn giao

Các file nhỏ, tài liệu, mẫu giao diện và logo PNG/ICO dùng ngay trên GitHub. Vì giới hạn tải lên của kết nối, **logo HDV gốc 2048×2048** và **ZIP v1.1** được bảo quản dưới dạng các phần `.part001`, `.part002`, ...; từng phần là byte gốc không mất dữ liệu.

Sau khi clone repository, chạy:

```bash
python scripts/restore_large_assets.py
```

Lệnh khôi phục `assets/HDV_LOGO_ORIGINAL_2048.png` và `release/C3D_TOOL_STANDARD_V1_1_HDV_LOGO.zip`, xác thực SHA256 tự động. Xem [hướng dẫn file lớn](LARGE_FILES.md).

**Phạm vi:** repository chứa tiêu chuẩn dùng chung, không chứa source, lệnh hoặc DLL nghiệp vụ riêng của bất kỳ tool nào.

## v1.2 — Danh mục thuật toán hiện hành

- **`ALGORITHM_INVENTORY.md`**: danh mục hiện hành của repo tiêu chuẩn (repo này không có mã nguồn tool, nên 0 thuật toán xác minh; không phải danh sách tool riêng).
- **`HUONG_DAN_DANH_MUC_THUAT_TOAN.md`**: quy định bắt buộc chỉ giữ tên/chức năng thuật toán trong phiên bản hiện tại.
- **`scripts/update_algorithm_inventory.py`**: tạo mới toàn bộ bảng từ metadata trong C#, so SHA256, `--check` chặn build/release nếu bị cũ.
- **`.github/workflows/check-algorithm-inventory.yml`**: kiểm tra đồng bộ trên mỗi push/PR.
- **`templates/ALGORITHM_INVENTORY.md`** và **`templates/ALGORITHM_METADATA.cs.txt`**: mẫu cho tool C3D mới.

**Tải ZIP chuẩn v1.2 trên GitHub:** gồm 9 phần dưới `release/`, dùng `python scripts/restore_large_assets.py` để ghép nguyên vẹn và kiểm tra hash. Bản v1.1 được giữ làm lịch sử tiêu chuẩn; danh mục thuật toán của từng tool **không giữ bản ghi thuật toán cũ**.

## Phạm vi khóa từ v1.3

- **Trong phạm vi:** đặc tả, thuật toán, UI dockable WebView2, CAD command, build DLL theo năm, test NETLOAD và DWG, source đầy đủ, dependency/resource, bảng thuật toán hiện hành.
- **Tách dự án:** các hình thức phân phối và tích hợp công cụ được xử lý ngoài bộ quy chuẩn này.
- **Tiêu chí bàn giao:** một thư mục DLL theo host có thể chọn `CadHost.dll` bằng NETLOAD; không được tuyên bố NETLOAD_PASS khi chưa thử trên Civil 3D thật.

## References Autodesk theo phiên bản, độc lập tool

- `references/<year>/`: chính sách và manifest tham chiếu được dùng cho bất kỳ công cụ nào cần Autodesk API, không giới hạn ở Brep hoặc một DLL cụ thể.
- `scripts/add_reference.ps1`: nhận tên assembly bất kỳ và năm host, đặt file hợp lệ vào kho tham chiếu cục bộ (DLL không đưa lên Git).
- Mỗi dự án chọn đúng các tham chiếu mình sử dụng, không ép mọi project dùng toàn bộ thư viện.
- Tất cả trạng thái build/NETLOAD được nghiệm thu theo từng dự án riêng; repository chuẩn không mang trạng thái thành công của dự án khác.
