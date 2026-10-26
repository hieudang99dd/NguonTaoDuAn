# QUẢN LÝ DANH MỤC THUẬT TOÁN HIỆN HÀNH — HDV C3D

**Đây là yêu cầu bắt buộc cho mọi tool Civil 3D mới hoặc khi sửa phiên bản cũ.**

## Mục tiêu

Mỗi tool có một file duy nhất ở thư mục gốc: `ALGORITHM_INVENTORY.md`, gồm hai cột **Tên thuật toán** và **Chức năng**. Chỉ thuật toán hiện có và đang dùng trong bộ mã nguồn mới nhất xuất hiện. Không giữ dòng thuật toán cũ, đã xóa, đã gộp, đã thay thế; Git có thể giữ lịch sử commit để truy xuất khi cần.

## Cách thực hiện

1. Sao chép `scripts/update_algorithm_inventory.py` vào thư mục `scripts/` của tool.
2. Đánh dấu thuật toán thực tế trong file `.cs`:

   ```csharp
   // HDV-ALGO-NAME: SurfaceSolidCreator
   // HDV-ALGO-FUNCTION: Tạo Solid từ bề mặt được chọn bằng API Civil 3D.
   ```

   Nếu nhiều thuật toán cùng file, có thể có nhiều cặp tên/chức năng. Ghi metadata cho mọi `.cs` thực thi thuật toán trong `Algorithms/`; các nơi khác ghi metadata nếu file thực sự triển khai thuật toán.
3. Sau **mỗi lần thêm, sửa, xóa, gộp, thay thế**: cập nhật metadata mô tả đúng hành vi rồi chạy:

   ```bash
   python scripts/update_algorithm_inventory.py --source-root src
   ```

4. Trước commit, build 2024/2025, đóng ZIP, gửi bàn giao:

   ```bash
   python scripts/update_algorithm_inventory.py --source-root src --check --require-source
   ```

5. Trong CI, dùng `.github/workflows/check-algorithm-inventory.yml`; phiên bản tiêu chuẩn không có mã nguồn tool nên CI mặc định không dùng `--require-source`, còn CI của tool thật **phải thêm `--require-source`**. Kết quả FAIL chặn merge/release.

## Cơ chế làm mới

- Script **ghi lại toàn bộ bảng** từ `.cs` được quét, không chắp thêm nội dung cũ.
- Đổi/tái cấu trúc thuật toán: sửa tên/chức năng trong metadata + chạy lại script; tên cũ biến mất.
- Xóa source cũ: dòng tương ứng biến mất; nguồn cũ không được để trong thư mục `src` active hoặc gói phát hành.
- Thay đổi bất kỳ phần nào của `.cs` có thuật toán: SHA256 nhúng kín trong file danh mục đổi → `--check` FAIL cho đến khi chạy sinh lại.
- Chặn tên trùng; chặn file `.cs` trong `Algorithms/` thiếu chú thích; chặn đánh dấu `HDV-ALGO-STATUS` không phải active.

## Giới hạn và nghiệm thu

Tool Python **không tự hiểu nghiệp vụ thuật toán C#**. Vì thế bắt buộc review thủ công để chứng minh chức năng mô tả đúng code thực và không bỏ sót thuật toán trong các file `.cs` ngoài thư mục `Algorithms/` không có metadata. Với dự án custom non-SDK hoặc `Compile Remove`, cung cấp `--compiled-files path/to/compiled_files.txt` có đường dẫn các file thực sự được biên dịch để tránh đưa source không sử dụng vào danh mục.

**Không tự khẳng định một tool đã có thuật toán chỉ từ tài liệu kế hoạch.** Repository này là bộ tiêu chuẩn, không phải source code đầy đủ của từng tool.
