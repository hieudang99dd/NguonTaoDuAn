# QA CHECKLIST — TOOL CIVIL 3D / HDV

Tên tool: __________  Version: __________  Command: __________  Chủ sở hữu nghiệm thu: __________

| ID | Gate / Bài kiểm tra | 2024 | 2025 | 2026 | Bằng chứng / log |
|---|---|---|---|---|---|
| G0 | Đọc ZIP gốc, đối chiếu changelog, command, phụ thuộc | NOT_RUN | NOT_RUN | NOT_RUN | |
| G1 | Đầu vào/đầu ra + ma trận chức năng & nghiệm thu | NOT_RUN | NOT_RUN | NOT_RUN | |
| G2 | UI preview dark/orange, dock hẹp, DPI, button flow | NOT_RUN | NOT_RUN | NOT_RUN | |
| G2-L1 | Logo HDV từ `assets/HDV_LOGO_ORIGINAL_2048.png`, đúng tỷ lệ, không cắt/méo | NOT_RUN | NOT_RUN | NOT_RUN | |
| G2-L2 | Logo + tên tiếng Anh đầy đủ trên Palette, dock 350–430 px, DPI 100–200% | NOT_RUN | NOT_RUN | NOT_RUN | |
| G3 | UI ↔ IPC action mapping + mock | NOT_RUN | NOT_RUN | NOT_RUN | |
| G4 | Unit engine, geometry, units, batch, error/cancel | NOT_RUN | NOT_RUN | NOT_RUN | |
| G5 | Document lock/command context/transaction/Undo/SaveAs | NOT_RUN | NOT_RUN | NOT_RUN | |
| G6a | BuildKit verify + doctor đúng references | NOT_RUN | NOT_RUN | NOT_RUN | |
| G6b | Full build CadHost + dependencies + resources | NOT_RUN | NOT_RUN | NOT_RUN | |
| G6c | Log sạch, TFM đúng, SHA256, không DLL giả | NOT_RUN | NOT_RUN | NOT_RUN | |
| G7a | NETLOAD CadHost.dll + chạy lệnh, mở PaletteSet | NOT_RUN | NOT_RUN | NOT_RUN | |
| G7b | WebView2 Runtime, chọn CAD, đổi DWG, đóng/mở palette | NOT_RUN | NOT_RUN | NOT_RUN | |
| G7c | Kết quả DWG thực chính xác và đối chiếu native | NOT_RUN | NOT_RUN | NOT_RUN | |
| G7d | Batch có lỗi một phần, rollback, cleanup, undo | NOT_RUN | NOT_RUN | NOT_RUN | |
| G8-L1 | Logo/icon hiển thị thực tế trên Ribbon/installer nếu tích hợp, đúng resource và kích thước | NOT_RUN | NOT_RUN | NOT_RUN | |
| G8 | EXE/bundle/Ribbon + update/uninstall/rollback Windows | NOT_RUN | NOT_RUN | NOT_RUN | |

**Kiểm tra bổ sung:** SHA256 logo gốc trong ZIP phải trùng file người dùng cung cấp; không đánh giá Ribbon/EXE `PASS` khi chưa tích hợp vào binary/Windows.

**Ký hiệu:** `PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`, `N/A`. Ghi hostname build, host patch, framework, test DWG, số lượng đối tượng, log/ảnh trước khi đổi `NOT_RUN` thành `PASS`.

**Quy tắc bàn giao:** `BUILD_PASS` không tương đương `NETLOAD_PASS`; `NETLOAD_PASS` không tương đương `CAD_PASS`; mock installer không tương đương `INSTALL_PASS`.
