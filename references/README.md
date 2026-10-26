# Autodesk API reference store — dùng chung mọi tool Civil 3D

Đây là **quy trình nền tảng**, không phải bộ mã nguồn SLB/QSL/Cutter hay bất kỳ tool nghiệp vụ nào.

## Nguyên tắc

- Mỗi host 2024, 2025, 2026 có thư mục `references/<year>/` riêng, không trộn assembly khác năm.
- Chỉ nhập DLL có quyền sử dụng từ máy cài AutoCAD/Civil 3D hoặc Autodesk SDK hợp lệ. **Repository công khai không chứa DLL Autodesk**.
- Tên file, SHA256, PE format và năm được khai báo là **kiểm tra bước đầu**, không thể tự khẳng định phiên bản Autodesk, chữ ký nhà phát hành, tương thích runtime hoặc kết quả NETLOAD.
- Tham chiếu Autodesk ở CadHost đặt `Private=false` / `Copy Local=false`. Trong sản phẩm NETLOAD chỉ mang DLL của tool và dependency riêng có quyền phân phối, không chép lại Autodesk DLL.
- Project nào cần assembly nào thì kê khai chính assembly đó; không bắt buộc mọi tool có cùng bộ DLL.

## Nhập thư viện cục bộ

```powershell
python scripts/reference_manager.py import --year 2025 --source "C:\AutodeskRefs\MyAssembly.dll"
```

Hoặc dùng PowerShell không cần Python:

```powershell
.\scripts\add_reference.ps1 -Year 2025 -SourceDll "C:\AutodeskRefs\MyAssembly.dll"
```

Cả hai cách giữ file trên **máy build**, không commit binary vào GitHub. Nếu file đã tồn tại mà khác hash, phải xác nhận thay thế (`--replace` hoặc `-Replace`).

## Kiểm tra thư viện trước khi build

```powershell
python scripts/reference_manager.py check --year 2025 --require AcMgd.dll --require AcDbMgd.dll
python scripts/reference_manager.py check --year 2025 --project "C:\Source\CadHost.csproj"
python scripts/reference_manager.py check --year 2025 --requirements-json "C:\Source\references.required.json"
python scripts/reference_manager.py list --year 2025
```

`references.required.json` do **từng tool** cung cấp, ví dụ `{"requiredAssemblies":["AcMgd.dll","AcDbMgd.dll"]}`. Bộ chuẩn không lưu requirements cho bất kỳ tool cụ thể nào.

Script quét các `Reference Include` phổ biến của Autodesk trong `.csproj`, nhưng không thể tự suy ra 100% assembly cần thiết chỉ từ C# `using`. Vì vậy, đối với kiểu/API đặc biệt, luôn bổ sung dependency vào `requiredAssemblies` và chạy kiểm tra.

## Tích hợp csproj

Với assembly `MyAssembly.dll` của năm host mục tiêu:

```xml
<Reference Include="MyAssembly">
  <HintPath>$(C3DReferenceRoot)\MyAssembly.dll</HintPath>
  <Private>False</Private>
</Reference>
```

`C3DReferenceRoot` do dự án đặt đến `references/<year>` tương ứng; cấu hình đúng TFM và kiến trúc theo phiên bản Civil 3D. Mọi lần thêm/sửa API đều chạy preflight rồi mới build.

## Kiểm thử / giới hạn

`REFERENCE_CHECK_PASS` chỉ xác nhận file **đã kê khai** có mặt và có header PE hợp lệ, hash không thay đổi so với index cục bộ. Đây **không** phải `BUILD_PASS`, `NETLOAD_PASS`, hay `CAD_PASS`. Để nghiệm thu phải biên dịch với bộ reference đúng năm và kiểm thử trong Civil 3D thực tế.

## Hai môi trường 2025

AutoCAD 2025 trước Update 1.4: .NET8. AutoCAD 2025 Update 1.4 trở lên: .NET10 (kèm cập nhật Civil 3D phù hợp, ví dụ Civil 3D 2025.2.7). **Không trộn Autodesk refs .NET8 với .NET10 trong cùng một cấu hình build**. Phân loại kho 2025 theo profile patch/framework trên máy build; manifest năm không tự quyết định TFM. `buildkit_bridge.py inspect --host-runtime net10` đọc metadata, nhưng BuildKit 1.0 cần nâng cấp trước khi biên dịch net10.
