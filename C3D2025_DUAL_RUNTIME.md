# Civil 3D 2025 — hai cấu hình .NET 8 / .NET 10 dùng chung một mã nguồn

**Phạm vi:** mọi plugin Civil 3D C# chạy trực tiếp bằng NETLOAD, không phụ thuộc một tool cụ thể.

## Vì sao cần hai profile?

- AutoCAD 2025 đến Update 1.3 chạy .NET 8; từ Update 1.4 chuyển sang .NET 10. Đảm bảo các thành phần Civil 3D 2025 cùng máy được cập nhật tương thích.
- Autodesk nêu rõ hầu hết plugin .NET 8 hiện có có thể tiếp tục chạy sau chuyển đổi .NET 10, nhưng vẫn cần kiểm thử vì thay đổi breaking hoặc dependency có thể làm lỗi.
- Để bảo đảm khả năng bàn giao cho nhiều máy, chuẩn dự phòng là **một source, hai bản build CadHost riêng**. Không trộn .NET 8 và .NET 10 references, đặc biệt không chọn bộ chỉ dựa vào AssemblyVersion=25.0.0.0.

## Nguồn duy nhất, 2 bộ tham chiếu, 2 DLL đầu ra

```text
ToolSource/
  src/ (Domain, Application, Infrastructure, CadHost dùng chung)
  buildkit.project.json / *.sln / *.csproj
NguonTaoDuAn/ (repo chuẩn)
  references/2025/net8/  # Autodesk assemblies được cấp quyền, KHÔNG commit
  references/2025/net10/ # Autodesk assemblies được cấp quyền, KHÔNG commit
Deliverables/
  C3D2025-NET8/Tool.CadHost.dll + dependencies/UI tương ứng
  C3D2025-NET10/Tool.CadHost.dll + dependencies/UI tương ứng
```

### Nhập thư viện tham chiếu

```powershell
python scripts/reference_manager.py import --year 2025 --runtime net8 --source "C:\\LicensedAutodesk\\NET8\\AcDbMgd.dll"
python scripts/reference_manager.py import --year 2025 --runtime net10 --source "C:\\LicensedAutodesk\\NET10\\AcDbMgd.dll"
python scripts/reference_manager.py check --year 2025 --runtime net8 --requirements-json "C:\\Tool\\references.required.json"
python scripts/reference_manager.py check --year 2025 --runtime net10 --requirements-json "C:\\Tool\\references.required.json"
```

Lệnh import hiện kiểm tra PE/hash, không tự xác nhận framework đúng. **Trước build phải kiểm tra metadata TFM, Autodesk publisher, host patch/version, x64**. Khi có BuildKit v1, inspect metadata bằng:

```powershell
python scripts/buildkit_bridge.py inspect --kit "C:\\BuildKit" --year 2025 --host-runtime net10 --dll "C:\\LicensedAutodesk\\NET10\\AcDbMgd.dll"
```

Script inspect đọc thông tin DLL, không đồng nghĩa BuildKit v1 có thể build net10.

### Cấu hình CadHost

Có thể dùng `TargetFrameworks=net8.0-windows;net10.0-windows` với SDK-style csproj khi tương thích; mỗi target trỏ đến bộ Autodesk references cùng runtime. Xem `templates/C3D2025_DUAL_TARGET.csproj.txt` làm mẫu; **không coi template là một solution đã biên dịch**.

Build nhánh net8 bằng BuildKit 1.0 đã kiểm toán (hoặc SDK/MSBuild phù hợp). Build nhánh net10 yêu cầu **.NET 10 SDK/reference packs**, tập hợp Autodesk 2025 .NET 10 tương ứng và pipeline MSBuild/BuildKit mở rộng. Không sử dụng BuildKit net8 để biên dịch net10.

### Cách NETLOAD trên mỗi máy

- Xem phiên bản trong lệnh `ABOUT`. Với các máy AutoCAD 2025 trước Update 1.4, NETLOAD DLL trong `C3D2025-NET8`.
- Với các máy đã cập nhật đồng bộ AutoCAD 2025.1.4+ và Civil 3D liên quan, NETLOAD DLL trong `C3D2025-NET10`.
- Hai DLL có thể trùng tên, nhưng **không nạp đồng thời cả hai trong một phiên Civil 3D**, tránh lẫn assemblies/types; không trộn thư mục runtime.
- Một DLL `net8` có thể được dùng chung cho cả hai máy **chỉ khi** NETLOAD, UI/WebView2, geometry, undo và các use cases đều đạt trên cả hai môi trường. Không bảo đảm mặc định.

### Bộ thử nghiệm bắt buộc

| Bài kiểm tra | C3D 2025 .NET8 | C3D 2025 .NET10 |
|---|---|---|
| References đúng TFM và đúng bản cập nhật | NOT_RUN | NOT_RUN |
| Biên dịch CadHost và dependencies | NOT_RUN | NOT_RUN |
| NETLOAD và lệnh CommandMethod | NOT_RUN | NOT_RUN |
| PaletteSet/WebView2 và tài nguyên | NOT_RUN | NOT_RUN |
| Thao tác DWG, Undo, lỗi và phục hồi | NOT_RUN | NOT_RUN |

Ghi trạng thái BUILD_PASS, NETLOAD_PASS, CAD_PASS **riêng cho từng profile**. Không lấy kết quả NET8 thay cho NET10.

Nguồn chính thức:
- Autodesk AutoCAD 2025 managed .NET compatibility: https://help.autodesk.com/cloudhelp/2025/ENU/AutoCAD-Customization/files/GUID-A6C680F2-DE2E-418A-A182-E4884073338A.htm
- Autodesk Developer Blog (24/07/2026): https://blog.autodesk.io/autodesk-desktop-products-2025-2026-net-10-updates/
- Autodesk guidance on mixed version crashes: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/AutoCAD-2026-1-2-and-Toolset-Products-Crashes-After-Updating-To-NET-10-Based-Builds.html
