# Autodesk Civil 3D 2025 — local build references

Thư mục này dành cho các **assembly tham chiếu phục vụ biên dịch** (không phải DLL phân phối kèm sản phẩm).

Cần bổ sung `acdbmgdbrep.dll` để biên dịch mã sử dụng `Autodesk.AutoCAD.BoundaryRepresentation.Brep`.

- File đã được người dùng cung cấp để kiểm tra: `acdbmgdbrep.dll` (PE32+ x64, .NET assembly; dung lượng 178,008 bytes).
- SHA256 của file đã kiểm tra: `61a95900aa82c41a318e9c0f3feee5fda3c7ee8a9640c0794b5240732a15c67d`.
- Không đưa các DLL có bản quyền Autodesk vào repository công khai. Copy từ bộ Civil 3D 2025 hoặc Autodesk SDK đã được cấp quyền trên máy build.
- Dùng `scripts/install_c3d2025_brep_reference.ps1 -SourceDll "C:\duong-dan\acdbmgdbrep.dll"` để đặt thư viện vào `references/2025/` trên máy build.
- Trong cấu hình `.csproj` của CadHost 2025, thêm reference đến `references/2025/acdbmgdbrep.dll`, thiết lập `Private=False`.
- Không đưa file Autodesk API DLL này vào gói NETLOAD phát hành. Runtime Civil 3D sẽ cung cấp thư viện nền tảng của Autodesk.

Lưu ý: tên phiên bản trong file chưa đủ chứng minh tương thích với mọi bản cập nhật Civil 3D 2025; cần build và NETLOAD thực tế.
