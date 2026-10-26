# Thư viện tham chiếu Autodesk — Civil 3D 2025

Đây là **kho tham chiếu biên dịch dùng chung** cho mọi ứng dụng Civil 3D 2025, không dành riêng cho một dự án hoặc một API.

Mỗi tool khai báo đúng assembly cần dùng trong cấu hình build của chính tool đó. Có thể bao gồm các thư viện như `AcMgd.dll`, `AcDbMgd.dll`, `AcCoreMgd.dll`, `AeccDbMgd.dll`, `AecBaseMgd.dll`, `AecPropDataMgd.dll`, `acdbmgdbrep.dll` hoặc thư viện khác theo API thực tế. Danh sách ví dụ **không phải bộ tham chiếu bắt buộc**.

Đưa một DLL tham chiếu hợp lệ từ môi trường Autodesk đã được cấp quyền vào kho cục bộ:
```powershell
.\scripts\add_reference.ps1 -Year 2025 -SourceDll "C:\AutodeskReferences\acdbmgdbrep.dll"
```

Script dùng chung cho mọi assembly và năm phiên bản, không phân phối file Autodesk có bản quyền. Trong `.csproj`, trỏ `HintPath` đến thư mục `references/2025` và đặt `Private=False` cho reference Autodesk. Kiểm tra kiến trúc, version, framework và NETLOAD thực tế; không coi bản tham chiếu của năm khác là tương thích đương nhiên.
