# C3D TOOL DEVELOPMENT STANDARD — QUY TRÌNH CHUẨN TẠO TOOL CIVIL 3D

![Logo HDV chính thức](assets/HDV_LOGO_256.png)

**HDV — CIVIL 3D TOOL DEVELOPMENT STANDARD**  
**Quy chuẩn nhận diện:** giữ logo HDV gốc, bố trí logo đi cùng **tên tiếng Anh đầy đủ** của từng tool.

**Mã:** C3D-SOP-001  
**Phiên bản:** 1.1.0 — bổ sung nhận diện logo HDV  
**Ngày:** 26/10/2026  
**Phạm vi:** các công cụ C#/.NET hoạt động trong Autodesk AutoCAD/Civil 3D, ưu tiên 2024/2025, chuẩn bị mở rộng 2026.  
**Nhãn trạng thái:** TÀI LIỆU QUY TRÌNH / chưa phải DLL mới, chưa thay đổi mã nguồn tool cũ.

## 0. Nguồn đầu vào và cấp độ xác minh

- **Đã đọc trực tiếp từ ZIP:** `SolidBuilder_SLB_v4_4_0_DOCKABLE_2024_2025_FULL_SOURCE_BUILT_DLL.zip` (mã nguồn, tài liệu, 2 bộ DLL, báo cáo build), `HDVQ_SolidQuantity_v0_7_2_2024_2025_FULL_FIX.zip` (mã nguồn, DLL, UI, hướng dẫn lỗi WebView2), `HDV_C3D_BuildKit_1_0_OFFLINE.zip` (công cụ biên dịch và manifest), `HVDTools_RibbonPro_2025_FULL_SOURCE.zip` (mã nguồn installer/updater, tài liệu), `PROJECT_MASTER_SOURCE.md` và đặc tả `SOLID_CUTTER_PRO_TECHNICAL_SPEC_V1.md`, `ATGT_Quantity_Revision_Manager_Spec_v1_1.md`.
- **Phát hiện nhưng chưa đọc trực tiếp byte ZIP tại lần tổng hợp:** QSL v0.8.2, SolidCutterPro v2.3, SolidInfo v4.4, SolidLayer v1.1. Các mục liên quan lấy từ lịch sử yêu cầu/tên phát hành, không suy thành chứng nhận code mới nhất.
- **Xác minh cần tách:** mã đã có (IMPLEMENTED), kiểm tra tĩnh (STATIC_PASS), biên dịch (BUILD_PASS), NETLOAD trên host thật (NETLOAD_PASS), chạy nghiệp vụ trên DWG (CAD_PASS), installer/Ribbon thực tế (INSTALL_PASS). Không dùng chữ “hoàn thiện” thay các minh chứng riêng.

## 1. Nguyên tắc bất biến

1. **Yêu cầu mới nhất là chuẩn chốt:** ưu tiên yêu cầu trực tiếp > yêu cầu hiện hành trong project > file master > mặc định.
2. **Đọc nguyên bản:** không sửa ZIP trước khi lập danh mục file, mã nguồn, phụ thuộc, API và trạng thái đã nghiệm thu.
3. **Không phá luồng đã hoạt động:** mỗi chỉnh sửa có ma trận tác động và kiểm thử hồi quy, không tự thêm chế độ ngoài phạm vi.
4. **Thuật toán ẩn sau giao diện:** UI chỉ chứa đầu vào, lựa chọn, tác vụ, tiến trình, kết quả, không đưa chi tiết hình học/dung sai/cache/solver cho người vận hành.
5. **Mọi thao tác CAD là giao dịch an toàn:** phân biệt đọc/ghi, đúng Document, command context, transaction, rollback. Không sửa model từ event WebView2.
6. **Giữ bản vẽ an toàn:** mặc định không xóa/chỉnh dữ liệu nguồn; “Làm mới” chỉ xóa phiên giao diện; “Áp dụng” mới thay đổi DWG, có xác nhận và Undo hợp lý khi có ghi đè/xóa.
7. **Không báo thành công giả:** không coi không ném exception là thành công; phải xác minh output (ObjectId, loại, số lượng, thể tích, topology hoặc thuộc tính theo đặc thù).
8. **Không viện cớ thiếu Visual Studio:** kiểm tra HDV C3D BuildKit, chạy `verify`, `doctor` rồi build; thiếu tài nguyên phải chỉ rõ file/phiên bản.
9. **Mã nguồn hoàn chỉnh và artifact build thật:** không đưa file nguồn rời rạc, DLL giả, path ZIP chưa tồn tại hoặc source-only dưới tên built DLL.
10. **Không phân phối Autodesk API DLL trong plugin end-user:** Autodesk references để build nội bộ. Giữ giấy phép, hash, danh sách dependency, không đưa private key/chứng chỉ vào ZIP.

## 2. Bước 00 — Tiếp nhận, khóa bản gốc

**Đầu vào:** ZIP cuối, đặc tả, DWG mẫu, logo chính thức `assets/HDV_LOGO_ORIGINAL_2048.png`, lệnh tắt, host năm, các lỗi tái hiện, tên đầy đủ tiếng Anh và nhãn tiếng Việt.

- Liệt kê file, version assembly, `CommandMethod`, UI, tài nguyên, tài liệu, kết quả build, hash SHA256.
- Xác định đúng ZIP baseline (không mặc định file tên mới nhất là bản chạy tốt nhất); tạo `SOURCE_AUDIT.md`, so sánh với yêu cầu mới nhất.
- Đọc `README.md`, `PROJECT_STATUS.md`, `CHANGELOG.md`, các file `.csproj`, `buildkit.project.json`, `tool.json`.
- Chốt một mã lệnh CAD chính **duy nhất cho mỗi tool**, kiểm tra không trùng lệnh đang cài trong HVDTools/Ribbon. Ví dụ SLB; QSL cần xác định đúng nghiệp vụ sau khi đổi từ HDVQ; Solid Cutter phiên bản cũ dùng SLCUT.
- Đối chiếu thực tế source và changelog (bản HDVQ 0.7.2 vẫn có README nói “source candidate” dù ZIP đã có DLL: phải cập nhật tài liệu cho đúng artifact thực tế).

**Gate G0:** nguồn gốc, phạm vi, hệ phiên bản, lệnh CAD và tình trạng test rõ ràng.

## 3. Bước 01 — Đặc tả đầu vào → đầu ra → nghiệm thu

Tạo `FUNCTION_MATRIX.md` với bảng:

| ID | Đầu vào DWG | Tùy chọn UI | Engine/use case | Output | Điều kiện đạt | Điều kiện lỗi |
|---|---|---|---|---|---|---|
| F01 | đối tượng hợp lệ | lựa chọn cần thiết | thuật toán C# | Solid/metadata/report | output kiểm chứng được | hủy, nguồn đổi, giao hình không hợp lệ |

Ràng buộc phải nêu rõ:
- Phạm vi chọn: Model Space, Paper Space, block/Xref, từng đối tượng/nhiều đối tượng/tất cả, lọc theo layer/code/name.
- Hình học: hệ tọa độ WCS/UCS, X/Y/Z đầu-cuối, station/offset, tim tuyến; geometry valid/invalid, vùng hở/kín, dải độ cao, giao cắt, tolerance theo đơn vị.
- Dữ liệu: INSUNITS=0, phân loại m³/m²/cái, xử lý mixed units; nguồn tham chiếu có bị thay đổi hay không.
- Trạng thái dữ liệu: nhiều DWG, Save As, undo/redo, duplicate, stale snapshot, lệnh bị hủy.
- Kết quả: số đối tượng, thể tích, phân loại, layer, màu, metadata, log, Excel và nơi lưu.

**Gate G1:** mỗi chức năng có tình huống đúng/sai/hủy, chấp nhận được bằng DWG thử nghiệm.

## 4. Bước 02 — Thiết kế UI trước khi tích hợp

**Host mặc định:** `Autodesk.AutoCAD.Windows.PaletteSet` + WPF WebView2; dock trái/phải, thả nổi, cho phép thay đổi chiều rộng; không dùng Windows Form modeless làm giao diện sản phẩm cuối nếu mục tiêu là panel dockable.

**Nhận diện:** nền tối `#15191e`, cam `#f08b36` (tham chiếu SLB), màu phụ trung tính. Dùng **logo HDV được cung cấp tại `assets/HDV_LOGO_ORIGINAL_2048.png`**, không tự vẽ lại, thay màu hoặc đổi chữ; logo đi cạnh **tên tool tiếng Anh đầy đủ**. Tiêu đề/nhãn tác vụ chính vẫn dùng tiếng Việt ngắn gọn, đúng thuật ngữ Civil 3D.

**Bố cục:** tiêu đề/logo → chọn nguồn → các điều kiện cần thiết → thao tác → **Kết quả cuối cùng**; vùng điều khiển cuộn riêng và footer hành động/trạng thái cố định. Tham chiếu SLB: palette 430×730, tối thiểu 350×480, kiểm tra ở DPI 100–200%, panel hẹp.

**Thành phần bắt buộc tùy nghiệp vụ:**
- Nút chọn đối tượng trong DWG, chọn tất cả/lọc, danh sách có trạng thái trống/hết dữ liệu; không đưa quá nhiều công tắc kỹ thuật.
- `Áp dụng` ghi lên DWG; `Xuất` tạo file dữ liệu/Excel riêng; `Làm mới` reset giao diện và lựa chọn, không xóa/sửa DWG.
- Progress xác định theo đối tượng/cặp/phase thật; nếu không biết tổng thì dùng busy/indeterminate, **không giả %**.
- Lỗi rõ ràng, thông báo số lượng thành công/thất bại, khả năng xem/chọn đối tượng kết quả, không che bản vẽ; giữ kết quả từng phần nếu được phép.
- Mặc định bảng kết quả là bước cuối, không có review trùng, không có slogan “tiện ích cho kỹ sư”, không phô diễn tên thuật toán/dung sai.

**Gate G2:** HTML preview thể hiện đúng luồng và các trạng thái; xác nhận preview không phải ứng dụng CAD thật. **Bắt buộc:** logo HDV chuẩn, tên tool tiếng Anh đầy đủ, hiển thị đúng tại 350–430 px palette; không bị méo/cắt/chồng nút.


### 4.1. Chuẩn logo HDV dùng xuyên suốt vòng đời tool (mới v1.1)

| Điểm xuất hiện | Tệp đề xuất | Quy tắc bắt buộc |
|---|---|---|
| Tiêu đề PaletteSet / WebView2 | `assets/HDV_LOGO_64.png` hoặc `_128.png` | Hiển thị logo cạnh **tên tool tiếng Anh đầy đủ**; ảnh `object-fit:contain`, không méo, không ép toàn bộ tên thành `HDV` |
| Ribbon / thanh công cụ | `assets/HDV_LOGO_32.png` (hoặc 16/64 theo hệ icon) | Logo thương hiệu thống nhất, **nhãn Ribbon phản ánh đúng nghiệp vụ**; xác minh CUIX/host hỗ trợ định dạng icon; không thay `ribbonIcon` khi updater chưa hỗ trợ file icon |
| Bộ cài và trình cập nhật | `assets/HDV_TOOLS.ico`, `_256.png` | Logo hiển thị khi quy trình đóng gói Windows thật hỗ trợ; EXE chỉ được xem là đã nhúng icon sau khi kiểm tra resource trên binary và giao diện thực |
| README / SOP / tài liệu nghiệm thu | `assets/HDV_LOGO_256.png` | Tên nhóm HDV ở đầu tài liệu, ghi chú rõ build/mock/CAD-pass |
| ZIP bàn giao source / deploy | `assets/HDV_LOGO_ORIGINAL_2048.png` + PNG nhỏ | Asset thuộc package, đường dẫn tương đối ổn định, không phụ thuộc hình từ web |
| Hình xem trước / giới thiệu tool | `_256.png` hoặc `_512.png` | Giữ màu/độ tương phản/bố cục gốc, không chèn khẩu hiệu hoặc làm biến dạng logo |

**Quy tắc triển khai:** file gốc 2048×2048 phải giữ nguyên byte/hash; chỉ thu nhỏ tạo bản cho UI. Tránh kéo giãn, cắt chữ H/D, đổi màu hoặc gắn thêm chữ vào chính file logo. Trong thanh tiêu đề, tách riêng ảnh logo và text tên tool để nội dung chữ luôn sắc nét, không phải xử lý ảnh. Ảnh 16/32 px chỉ là fallback — kiểm tra độ nhận diện ở DPI thực; nếu thiếu rõ ràng, thiết kế icon đơn giản riêng trong một bước được phê duyệt (không tự sửa logo gốc).

**Tích hợp kỹ thuật:** `templates/branding.json` là metadata hướng dẫn, **không phải schema đã được CadHost hay HVDTools updater hỗ trợ**. Khi triển khai, nhúng image resources ở CadHost/WebView2, hoặc copy theo cấu trúc bundle để UI tìm thấy. Không mặc định đổi trường `ribbonIcon: "box"` thành đường dẫn PNG: updater hiện tại cần được mở rộng và test Windows trước khi làm vậy. Các namespace lịch sử `HDVQ`, `HVDTools` giữ nguyên cho đến khi có migration riêng; việc dùng logo HDV không tự động đổi command hoặc tên assembly.

**Điều kiện nghiệm thu nhận diện:** so ảnh gốc với file trong ZIP bằng SHA256; mở preview; thử panel hẹp/màn hình 100–200% DPI; kiểm tra `logo + full English name` trên Palette; kiểm tra icon thật trên Ribbon/EXE khi build/cài được; không đánh dấu PASS dựa trên ảnh minh họa.

## 5. Bước 03 — Kiến trúc 4 lớp cố định

```text
<Tool>/
├── <Tool>.sln / <Tool>.slnx
├── src/
│   ├── <Tool>.Domain/                # models, value objects, quy tắc thuần
│   ├── <Tool>.Application/           # use cases, validation, hợp đồng IPC
│   ├── <Tool>.Infrastructure/        # repository, báo cáo/Excel, log, tích hợp
│   └── <Tool>.CadHost/               # Autodesk API, lệnh, PaletteSet, WebView2
│       ├── Commands/                # hàng đợi, CommandMethod, transaction
│       ├── Cad/                     # adapters và truy cập Document/Database
│       └── UI/web/                  # HTML/CSS/JS và assets
├── assets/                          # Logo HDV gốc + icon nhiều kích thước
├── tests/                           # unit, contract, UI mock, integration
├── docs/                            # SOP áp dụng, quyết định, QA, changelog
├── buildkit.project.json            # recipe portable năm host
├── tool.json                        # metadata cho Ribbon/installer (schema hiện hành)
├── branding.json                    # hướng dẫn nhận diện, chưa có runtime binding
├── PROJECT_STATUS.md
└── README.md
```

**Ranh giới:** Domain không phụ thuộc Autodesk DLL/WebView2. Application không gọi UI/CAD trực tiếp. Infrastructure triển khai interface có thể test độc lập. CadHost là adapter duy nhất chạm API Civil 3D, command context và PaletteSet. Với các thuật toán phụ thuộc trực tiếp AutoCAD geometry, tách `CadHost/Cad` hoặc một adapter host-specific; không cố ép chúng vào lớp thuần.

**Giao tiếp:** `WebRequest {requestId, action, payload, documentContext}` → validate → CadCommandQueue → CadActionDispatcher → engine → `WebResponse {requestId,status,payload,error}`. Trạng thái: `accepted/progress/completed/failed/cancelled`; chống double click, ghi log và không xử lý response cũ vào DWG khác.

**Gate G3:** chức năng map một-một từ nút UI đến handler và kết quả; mock IPC chạy được không cần Civil 3D.

## 6. Bước 04 — Phát triển engine nghiệp vụ

**Đối với tất cả tool:**
1. Validation đầu vào trước khi giao dịch, đủ thông tin lỗi cho từng đối tượng.
2. Nếu có API Native Autodesk đúng ý nghĩa nghiệp vụ thì ưu tiên sử dụng; không tự viết lại solver hình học khi không cần.
3. Các bộ xử lý dài phải có progress/cancel an toàn, log định danh công việc, xử lý lỗi từng phần hoặc atomic theo yêu cầu.
4. Trước commit, xác minh kết quả thật: type, số lượng, thuộc tính, hình học/vùng giao/volume, không xóa kết quả đã commit khi tác vụ khác thất bại.
5. Dùng temporary layer/objects có tên độc nhất, quản lý cleanup, không lẫn nguồn/chỉnh sửa file gốc. Khi cleanup thất bại phải báo rõ, không âm thầm trả completed.

**Khác biệt theo nhóm:**
- **SLB:** có hoặc không có Corridor; bề mặt tham chiếu và so sánh TIN có quyền lấy ngoài Corridor **độc lập**; dùng SurfaceId thực để xác định quan hệ, không so tên; tạo Solid bằng `TinSurface.CreateSolidsAtSurface`; lưu lại cặp nguồn, layer, kết quả; không tự bật engine sửa lưới TIN nếu người dùng đã bỏ yêu cầu này.
- **Solid Cutter:** phân biệt polyline kín/hở, tim XYZ lấy đúng cao độ đầu/cuối, hướng đục, chiều cao thủ công, solid cống; phải kiểm tra **thể tích/phần giao thực** khi Boolean Subtract. Cống tròn phải dựng khối cắt đặc theo biên dạng ngoài khi cần, không nhầm solid cống rỗng với cutting tool.
- **Quantity/SolidInfo:** scan 3DSOLID trong phạm vi đã chốt; xử lý nhiều solid cùng layer, lỗi ACIS/volume, đổi đơn vị INSUNITS, fingerprint để phát hiện kết quả cũ khi DWG bị chỉnh sửa; báo cáo Excel và metadata không đổi nguồn trừ khi `Áp dụng`.
- **SolidLayer:** chọn tất cả/lọc, import Excel map layer/màu, TrueColor và batch operation; thay đổi dữ liệu chỉ khi Áp dụng; xác nhận kết quả thật.
- **ATGT:** tách nhận dạng block/layer, đối chiếu CAD gốc/sửa, thay đổi hình học, quản lý revision, thống kê và ánh xạ tới Alignment/station/offset. `StationLocationResolver.cs` là phần tử thứ 31 đã chốt trong đặc tả, nhưng đặc tả không phải minh chứng build.

**Gate G4:** unit tests engine + sai số/điều kiện biên; tính đúng đắn theo nghiệp vụ không phụ thuộc UI.

## 7. Bước 05 — CadHost, tương tác CAD và IPC

- `CommandMethod("LENH_CHINH")` là lệnh duy nhất để gọi tool; lệnh nội bộ chẩn đoán tách khỏi thao tác sản phẩm, tránh va chạm lệnh giữa nhiều plugin.
- Chỉ truy cập Autodesk Database/Editor trong ngữ cảnh lệnh hợp lệ (`ExecuteInCommandContextAsync` hoặc cơ chế CAD command được kiểm chứng), không trong callback WebView2 thread. Thao tác modeless cần document context và `DocumentLock` khi thích hợp.
- Mỗi batch/transaction phải theo **đúng DWG đã chọn**; kiểm tra database identity mỗi lần chạy. Không cache `ObjectId` giữa session; Handle phải resolve/validate, không mặc định bền vững giữa clone/copy.
- `Transaction`/rollback theo phạm vi đơn hàng/cặp; `Undo` có kết quả có thể hoàn tác; chọn đối tượng bằng `Editor.GetSelection` có xử lý Cancel; không kéo theo UI treo/ẩn không mở lại.
- Khi DocumentActivated/DocumentDestroyed/SaveAs/Units thay đổi: invalidation catalog/snapshot; không hiển thị báo cáo của DWG cũ.
- JSON IPC phải versioned; reject payload không hợp lệ và request trùng, không sử dụng `crypto.randomUUID` khi WebView2 có opaque origin trừ khi có fallback.

**Gate G5:** UI mock và contract tests; không exception xuyên cầu giao tiếp, không đụng DWG khác.

## 8. Bước 06 — Build theo host và kiểm soát dependency

| Civil 3D | Target mặc định | Điều kiện |
|---|---|---|
| 2024 | `net48` | Autodesk references 2024 (AutoCAD 24.3), plugin x64 |
| 2025 | `net8.0-windows` | Autodesk references 2025 (25.0); kiểm tra bản Update/.NET transition thực tế |
| 2026 | profile riêng theo bản update | Kiểm tra .NET 8 hoặc .NET 10 và Autodesk references 2026; BuildKit v1 chưa hỗ trợ 2026 |

**BuildKit ưu tiên:** giải nén `HDV_C3D_BuildKit_1_0_OFFLINE.zip`; xem `START_HERE.md`, `BUILD_GUIDE.md`, `PAYLOAD_SHA256.json`. Chạy theo thứ tự:

```bash
python3 scripts/build.py verify
python3 scripts/build.py doctor --year 2024 --project /path/to/Tool/buildkit.project.json
python3 scripts/build.py build --project /path/to/Tool/buildkit.project.json --year 2024 --out /path/to/dist/2024
python3 scripts/build.py doctor --year 2025 --project /path/to/Tool/buildkit.project.json
python3 scripts/build.py build --project /path/to/Tool/buildkit.project.json --year 2025 --out /path/to/dist/2025
```

Trên Windows sử dụng `build.cmd`/`build.ps1` tương ứng theo tài liệu kit. `verify` xác nhận hash; `doctor` kiểm tra tham chiếu theo năm; `build` dùng Roslyn portable, **không đồng nghĩa MSBuild**. Nếu dự án dùng XAML/RESX/code generators/COM interop/NuGet khác recipe, chuyển qua pipeline VS/MSBuild có đầy đủ targeting packs và reference thật. Không tạo DLL thiếu resource chỉ để compile đạt.

**Quy tắc phụ thuộc:** `AcMgd`, `AcDbMgd`, `AcCoreMgd`, `AecBaseMgd`, `AeccDbMgd` theo đúng năm; `AecPropDataMgd` chỉ khi cần và đúng năm (bộ kit v1 thiếu `AecPropDataMgd` 2024). Autodesk references có `Private=false`/CopyLocal=false. Đóng gói đúng WebView2 Core/Wpf hoặc WinForms tùy host, loader x64, HTML/CSS/JS, Newtonsoft.Json/ClosedXML nếu sử dụng. WebView2 **SDK DLL không thay thế Edge WebView2 Runtime** của Windows.

**Gate G6:** 0 compile error, danh sách warning công khai, result.json, compiler log, metadata DLL/TFM, dll/dependencies/UI đầy đủ; không chép API Autodesk DLL làm thư viện chạy end-user.

## 9. Bước 07 — Kiểm thử 5 lớp và nghiệm thu

**A. Static/Unit:** compile, phân tích API, unit engine; sai lệch số học, dữ liệu trống, unicode, filename, layer, mã nguồn đầy đủ.

**B. IPC/UI:** mọi action, click/refresh/cancel, hàng đợi, dock/narrow, scrolling, overlay, preview vs CAD, lỗi `crypto.randomUUID`.

**C. NETLOAD trên Windows:** host năm đúng, `NETLOAD` CadHost, gọi lệnh, PaletteSet hiển thị, chọn được trong CAD, thư viện WebView2 load được. Nếu trắng trang: dùng chẩn đoán WebView2 Runtime, HRESULT, loader và profile `%LOCALAPPDATA%`, không tự suy là lỗi geometry.

**D. CAD/DWG:** DWG chuẩn/lỗi/nặng, nhiều DWG, chuyển tài liệu, ctrl+Z/undo, save/open, Xref, block, layer trùng tên, INSUNITS=0, WCS/UCS, các hình học sát/không giao/biên, các solid lớn và solid trụ/cống, chạy batch có phần thất bại. So output với công cụ Civil 3D Native khi nghiệp vụ tương đương.

**E. Installer/Ribbon:** chạy EXE trên máy Windows thử, xác minh đường dẫn bundle/cuiX, tab BIM TUYẾN và nhóm đúng, icon/tên đầy đủ, tự động load sau khởi động lại, update/thêm tool/rollback/uninstall, SECURELOAD/TRUSTEDPATHS giữ an toàn. Không khẳng định cài được nếu mới test mô phỏng CUIX trên Linux.

**Gate G7:** chỉ `CAD_PASS` khi có test thực trên đúng phiên bản; chỉ `INSTALL_PASS` khi EXE/Ribbon được kiểm tra thực trên Windows/C3D.

## 10. Bước 08 — Đóng gói 3 tầng

**Tầng 1 — Source package:** solution, toàn bộ `.cs`/UI/assets (bao gồm logo HDV gốc và biến thể nhỏ), recipe, tests, docs, license, hash, đầy đủ file bổ trợ; không kèm private key.

**Tầng 2 — NETLOAD package (mỗi năm):** thư mục có `*.CadHost.dll`, `Domain/Application/Infrastructure`, WebView2 assemblies/loader và UI/assets bao gồm logo HDV nếu không embedded, config, hướng dẫn NETLOAD, báo cáo phiên bản; không trộn 2024 với 2025.

**Tầng 3 — Product installation:** `tool.json`, `.bundle/PackageContents.xml`, CUIX/Ribbon hoặc RibbonHost, logo/icon Windows được build và xác minh, setup EXE/updater, installer log, backup/rollback. Update plugin riêng phải không ghi đè plugin khác cùng command ID.

**tool.json mẫu:** xem `templates/tool.json` (chỉ là mẫu, cần sửa `id`, `command`, `entryAssembly`, `supportedYears` đúng bản tool đã nghiệm thu).

**Gate G8:** bản tải về có nội dung thật, hash SHA256 và cây file kiểm tra được, cài đặt/reinstall/upgrade không làm mất plugin khác.

## 11. Bước 09 — Bàn giao và quản lý phiên bản

Bàn giao tối thiểu:

1. `Tool_FULL_SOURCE_<version>.zip`.
2. `Tool_NETLOAD_C3D2024_<version>.zip` và `Tool_NETLOAD_C3D2025_<version>.zip` (chỉ khi đã build).
3. `Tool_Setup_<version>.exe` hoặc `.bundle` (chỉ khi đã tạo); mọi file cần cài có trong payload.
4. `QA_REPORT.md` có ma trận 6 trạng thái; không đánh tráo MOCK thành CAD test.
5. `CHANGELOG.md`, `PROJECT_STATUS.md`, `README_NETLOAD.md`, `SHA256SUMS.txt`.
6. `CommandMethod` chính + tên đầy đủ tiếng Anh + **logo HDV theo asset chuẩn** + menu Ribbon chuẩn (nếu tích hợp thật).
7. Phương án nâng cấp/thêm tool: `Incoming/<tool>.zip` với `tool.json`, đóng CAD, updater, khởi động lại, verify command.

Quy ước version: `MAJOR.MINOR.PATCH`, một baseline tag cố định. Chỉ ghi “bản phát hành hoàn chỉnh” khi G0–G8 đã có bằng chứng, nếu chỉ G0–G6 thì phải ghi **BUILD CANDIDATE / CHƯA NGHIỆM THU CAD**.

## 12. Các lỗi từ dự án cần chặn từ đầu

| Lỗi đã gặp | Nguyên nhân/rủi ro | Tiêu chuẩn ngăn tái diễn |
|---|---|---|
| DLL có nhưng NETLOAD không được | host/runtime/API sai, dependency thiếu | build matrix theo năm + smoke test trên Windows |
| WebView2 trắng/Class not registered | WebView2 runtime COM hoặc loader/profile | preflight Runtime/HRESULT, log, không che lỗi |
| Làm mới xóa dữ liệu CAD | phân biệt UI state và DWG state không rõ | Reset UI-only, transaction chỉ khi Áp dụng |
| Toolbar/kết quả bị che khi dock hẹp | CSS thiếu scroll/fixed footer, DPI | resize/DPI matrix, footer cố định |
| Số lượng Solid sai khi cùng layer | grouping/selection/filter sai | test 21 Solid cùng layer, compare ObjectId/volume |
| Cắt không giao/đục cống tròn sai | cutting solid không đặc/không đúng Z, thiếu intersection | verify cutter shape, min/max Z và Boolean delta volume |
| Lỗi khi chuyển nhiều DWG | stale IDs/document context | pin database, reset catalog, revalidate |
| Solid native thất bại và tool báo xong | chỉ dựa vào API không ném exception | đếm returned IDs, validation hình học, per-job report |
| Cài EXE xong không thấy Ribbon | bundle/CUIX load hoặc version không khớp | Windows acceptance, CUILOAD, ribbon tab and command |
| ZIP nhãn “đã build” nhưng thiếu DLL | lẫn source-only với release | artifact hash + file tree + BUILD_PASS evidence |

## 13. Kiểm tra tình trạng thực tế của các baseline được đọc

- SLB 4.4.0: đã có 4 project + 2024/2025 DLL và báo cáo offline compiler, 27 mock UI tests; NETLOAD/ACIS chưa thử trên Civil 3D thật.
- HDVQ Solid Quantity 0.7.2: đã có source và hai thư mục DLL/2024/2025; có thay đổi chẩn đoán WebView2 COM. CadHost bản này dùng WinForms modeless, chưa thể coi đã đạt PaletteSet dockable tiêu chuẩn mới. Tên lệnh source là `HDVQ`, không tự đồng nhất với QSL phiên bản sau.
- HDV C3D BuildKit 1.0: có compiler portable và Autodesk ref 2024/2025; bản thân nó chưa phải môi trường Civil 3D chạy thật, thiếu tham chiếu AecPropDataMgd 2024, chưa support 2026.
- HVDTools RibbonPro 2025: có source installer/updater, tool.json và kiểm thử giả lập; chưa nghiệm thu tự động hiển thị Ribbon với Civil 3D Windows.
- ATGT v1.1 và Cutter v1 là tài liệu đặc tả, không tự coi là DLL build.
- ZIP QSL 0.8.2 / SolidCutter v2.3 / SolidInfo v4.4 / SolidLayer v1.1 chưa đọc được binary tại lần tổng hợp này, phải kiểm tra khi dùng làm baseline triển khai tiếp.

## 14. Mẫu yêu cầu dùng lại ở mọi hội thoại

> Đọc `PROJECT_MASTER_SOURCE.md` và `QUY_TRINH_CHUAN_TOOL_CIVIL3D.md`. Đọc ZIP/code gốc mới nhất hiện có, không suy nguồn khác. Xác định source audit, yêu cầu đã chốt, luồng UI dark/orange dockable, logo HDV gốc cạnh tên tiếng Anh đầy đủ (theo tài liệu `HUONG_DAN_SU_DUNG_LOGO_HDV.md`), lệnh duy nhất và 4 lớp Domain/Application/Infrastructure/CadHost. Chỉ dùng Autodesk DLL đúng năm và thực hiện BuildKit verify→doctor→build; test IPC/UI và kiểm tra đầu ra thực; chỉ công bố NETLOAD/CAD_PASS khi chạy trên Civil 3D thật. Khi hoàn tất, xuất full source, 2024/2025 CadHost DLL nếu build thành công, dependencies, test report, changelog, hướng dẫn NETLOAD và gói updater `tool.json` nếu yêu cầu; không tạo lệnh/đường dẫn/tuyên bố nghiệm thu giả.
