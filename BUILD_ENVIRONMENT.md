# MÔI TRƯỜNG BUILD CIVIL 3D DÙNG CHUNG — kiểm toán BuildKit 1.0

**Mục tiêu:** dùng chung một nền tảng build cho nhiều tool C3D, không buộc vào tên/thuật toán của bất kỳ tool nào. Phạm vi bàn giao của từng tool dừng ở DLL cho `NETLOAD` cùng dependency và source.

## Kết quả kiểm toán bộ BuildKit do người dùng cung cấp (27/10/2026)

Nguồn được kiểm tra trực tiếp: `HDV_C3D_BuildKit_1_0_OFFLINE.zip` của người dùng, 1.148 thành phần (kể cả thư mục), dung lượng nén xấp xỉ 113 MiB, dữ liệu giải nén xấp xỉ 288 MiB.

- Roslyn compiler 4.11.0; .NET Runtime 8.0.32 cho Linux x64 và Windows x64; reference packs net48, netstandard2.0, net8 + WindowsDesktop.
- Có Autodesk reference 2024 (5 DLL) và 2025 (6 DLL); **không có Autodesk reference 2026**.
- Bộ 2024 gồm `acmgd.dll`, `acdbmgd.dll`, `accoremgd.dll`, `AecBaseMgd.dll`, `AeccDbMgd.dll`; chưa có `AecPropDataMgd.dll`.
- Bộ 2025 gồm các DLL nói trên và `AecPropDataMgd.dll`; **chưa có `acdbmgdbrep.dll`**.
- `verify` trên nguyên bản: **PASS** theo PAYLOAD_SHA256.json.
- `doctor` cơ bản: **2024 READY** (AutoCAD API 24.3.0.0), **2025 READY** (25.0.0.0).
- 8 bài thử BuildKit: **8/8 PASS** trong môi trường Linux kiểm toán.
- Biên dịch lại recipe mẫu bốn project (Domain, Application, Infrastructure, CadHost): **BUILD_PASS 2024** và **BUILD_PASS 2025**.
- **NETLOAD_PASS/CAD_PASS = NOT_RUN**: không có phiên Civil 3D Windows thực trong môi trường kiểm toán.
- Hệ thống recipe portable dùng `scripts/build.py`/Roslyn; **không phải MSBuild đầy đủ** và không xử lý mặc định XAML/RESX/generators/COM/C++-CLI.

### Lưu ý quan trọng về thư viện bổ sung

DLL `acdbmgdbrep.dll` được cung cấp riêng có metadata `AssemblyVersion = 25.0.0.0`, nhưng `TargetFramework = .NETCoreApp,Version=v10.0` và x64. **Phân biệt cập nhật:** AutoCAD 2025 trước Update 1.4 dùng .NET 8; AutoCAD 2025 Update 1.4 trở lên dùng .NET 10. DLL này có metadata phù hợp *về framework* với nhánh AutoCAD 2025.1.4+; điều đó chưa chứng minh nguồn phát hành và các dependency đã đồng bộ. Không đưa DLL .NET10 vào **BuildKit v1 vốn cố định net8 cho 2025**, trừ khi nâng cấp cả bộ công cụ build và các tham chiếu tương ứng.

## Đâu là GitHub, đâu là bộ biên dịch?

1. **GitHub công khai:** quy trình, kiểm tra phụ thuộc, recipe mẫu, danh mục thuật toán, `scripts/reference_manager.py`, `scripts/buildkit_bridge.py`. Không có bộ nhị phân Roslyn/runtime/Autodesk references của BuildKit đã tải lên.
2. **BuildKit riêng:** ZIP hoặc thư mục đầy đủ người dùng có quyền sử dụng, giải nén trên máy build/hệ thực thi của cuộc trò chuyện. Đây là nơi có compiler, framework packs, Autodesk references.
3. **Nguồn tool cụ thể:** source ZIP, recipe và test DWG của dự án hiện hành (không lưu trong bộ quy chuẩn tổng quát).

**Không đồng nhất việc đọc file GitHub với việc đã có compiler+DLL nhị phân để chạy.** ChatGPT ở hội thoại mới chỉ sử dụng được BuildKit nếu file có thể truy cập trong môi trường đó (ví dụ file Project đính kèm, Library khả dụng hoặc người dùng gửi ZIP). Không khẳng định môi trường mọi hội thoại tự động dùng chung thư mục giải nén.

## Kết nối kho references với BuildKit

Sau khi clone bộ chuẩn và giải nén BuildKit (ví dụ: `C:\BuildTools\HDV_C3D_BuildKit`), trên máy có Python:

```powershell
python scripts/buildkit_bridge.py verify --kit "C:\BuildTools\HDV_C3D_BuildKit"
python scripts/buildkit_bridge.py doctor --kit "C:\BuildTools\HDV_C3D_BuildKit" --year 2025 --project "C:\Source\Tool\buildkit.project.json"
python scripts/buildkit_bridge.py build --kit "C:\BuildTools\HDV_C3D_BuildKit" --year 2025 --project "C:\Source\Tool\buildkit.project.json"
```

Nếu thiếu một DLL đã **kê khai** trong recipe, nhập thư viện hợp lệ vào `references/<year>/` cục bộ rồi **kiểm tra và đồng bộ**:

```powershell
python scripts/reference_manager.py import --year 2025 --source "C:\LicensedAutodesk\SomeApi.dll"
python scripts/buildkit_bridge.py sync --kit "C:\BuildTools\HDV_C3D_BuildKit" --year 2025 --project "C:\Source\Tool\buildkit.project.json"
```

`sync` chỉ sao chép các thư viện thực sự được recipe yêu cầu, đã kiểm tra metadata đúng framework và không được phép âm thầm ghi đè bản hash khác. Nếu framework không khớp *runtime của bản cập nhật CAD được chọn*, dừng trước build. Không coi mọi DLL .NET 10 là sai với AutoCAD 2025.

**Kiểm tra giới hạn:** Bridge kiểm tra TFM của DLL được recipe kê khai và tính toàn vẹn payload BuildKit. Không tự xác thực publisher, license, chữ ký Authenticode, API tương thích tuyệt đối hoặc hành vi CAD. Năm 2026 cần BuildKit profile mới; không dùng lại DLL 2025 dưới tên 2026.

## Chính sách GitHub

Không commit trực tiếp thư viện Autodesk do người dùng cung cấp lên kho public khi chưa có quyền phân phối. Không commit source của dự án nghiệp vụ vào repo tổng quát. Mọi nghiệm thu BUILD / NETLOAD / CAD ghi riêng và gắn với tool tương ứng.

## Đính chính 27/10/2026 — thay đổi quan trọng

Tài liệu Autodesk xác nhận AutoCAD 2025.1.4 và Civil 3D 2025.2.7 (cập nhật tương ứng) đã chuyển sang .NET 10 vào tháng 9/2026. Vì vậy AutoCAD/Civil 3D **2025 có hai profile**: bản cũ .NET8 và bản đã cập nhật .NET10. Các DLL 25.0.0.0 không đủ để chọn profile vì cùng major assembly version. DLL Brep do người dùng gửi nhắm .NET10 là điều phù hợp với hệ 2025 cập nhật, nhưng kiểm tra chữ ký và version các assembly nền tảng trong cùng bộ vẫn cần thiết. Bridge hỗ trợ đọc metadata với `inspect --year 2025 --host-runtime net10`, nhưng với BuildKit 1.0 hiện tại, `build/sync --host-runtime net10` báo thiếu profile build .NET10; **đây là giới hạn BuildKit, không phải lỗi DLL**.

Nguồn chính thức: https://help.autodesk.com/cloudhelp/2025/ENU/AutoCAD-WhatsNew/files/GUID-07450FCA-16CA-4D7A-8EA2-9CE842631D75.htm và https://blog.autodesk.io/autodesk-desktop-products-2025-2026-net-10-updates/ .
