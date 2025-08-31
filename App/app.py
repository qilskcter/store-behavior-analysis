import wx
from main import runApplication
from heatmap import runHeatmap
import json
from detech import runDetech
from os import startfile, path

class AnalystDialog(wx.Dialog):
    def __init__(self, parent, title, message_text):
        super(AnalystDialog, self).__init__(
            parent, title=title, size=(250, 150))
        panel = wx.Panel(self)
        self.btn = wx.Button(panel, wx.ID_OK, label="OK",
                             size=(80, 30), pos=(90, 65))
        self.message = wx.StaticText(panel, size=(200, 30), pos=(50, 30))
        self.message.SetLabelText(message_text)

    def set_message(self, message_text):
        self.message.SetLabelText(message_text)


class RTSPDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(RTSPDialog, self).__init__(parent, title=title, size=(300, 150))
        panel = wx.Panel(self)

        self.rtsp_label = wx.StaticText(panel, label="Enter RTSP Link:", pos=(10, 20))
        self.rtsp_text = wx.TextCtrl(panel, pos=(120, 20), size=(150, 25))

        self.ok_button = wx.Button(panel, wx.ID_OK, label="OK", size=(80, 30), pos=(110, 65))
        self.cancel_button = wx.Button(panel, wx.ID_CANCEL, label="Cancel", size=(80, 30), pos=(200, 65))


class AlertDialog(wx.Dialog):
    def __init__(self, parent, title, image_path):
        super(AlertDialog, self).__init__(parent, title=title)
        panel = wx.Panel(self)

        try:
            image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
            if image.IsOk():
                width, height = image.GetWidth(), image.GetHeight()
                self.SetSize((width + 20, height + 100))  # Adjust for borders and buttons
                wx.StaticBitmap(panel, -1, wx.Bitmap(image), pos=(10, 10))
            else:
                wx.MessageBox("Failed to load the image.", "Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

        ok_button = wx.Button(panel, wx.ID_OK, label="OK", size=(80, 30), pos=(width // 2 - 40, height + 20))
        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)

    def on_ok(self, event):
        self.Destroy()


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Report Analysis', size=(690, 550),
                         style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel = wx.Panel(self)

        icon_path = '../cctv.ico'
        icon = wx.Icon(icon_path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        panel.SetBackgroundColour(wx.Colour(185, 211, 238))

        bold_font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        store_text = wx.StaticText(panel, label="STORE BEHAVIOR ANALYSIS", pos=(140, 10))
        store_text.SetFont(bold_font)

        store_text.SetForegroundColour(wx.Colour(0, 0, 128))

        browse_icon_path = r'../icon/open-folder.png'
        heatmap_icon_path = r'../icon/heatmap.png'
        open_heatmap_icon_path = r'../icon/youtube.png'
        get_report_icon_path = r'../icon/schedule.png'
        open_excel_icon_path = r'../icon/excel.png'
        open_camera_icon_path = r'../icon/cctv.png'
        rtsp_icon_path = r'../icon/security-camera.png'
        alert_icon_path = r'../icon/alarm.png'

        icon_width = 45
        icon_height = 45

        icon_chieudai = 42
        icon_chieurong = 32

        wx.StaticText(panel, label="Mở Tệp", pos=(590, 290))
        wx.StaticText(panel, label="Phân tích Heatmap", pos=(60, 125))
        wx.StaticText(panel, label="Mở Heatmap", pos=(230, 125))
        wx.StaticText(panel, label="Đếm người", pos=(380, 125))
        wx.StaticText(panel, label="Mở Excel", pos=(530, 125))
        wx.StaticText(panel, label="Mở Camera", pos=(160, 220))
        wx.StaticText(panel, label="Sử dụng RTSP/HTTP Link", pos=(275, 220))
        wx.StaticText(panel, label="Cảnh báo", pos=(457, 220))

        browse_icon_image = wx.Image(browse_icon_path, wx.BITMAP_TYPE_PNG).Scale(icon_width, icon_height)
        heatmap_icon_image = wx.Image(heatmap_icon_path, wx.BITMAP_TYPE_PNG).Scale(icon_width, icon_height)
        open_heatmap_icon_image = wx.Image(open_heatmap_icon_path, wx.BITMAP_TYPE_PNG).Scale(icon_width, icon_height)
        get_report_icon_image = wx.Image(get_report_icon_path, wx.BITMAP_TYPE_PNG).Scale(icon_width, icon_height)
        open_excel_icon_image = wx.Image(open_excel_icon_path, wx.BITMAP_TYPE_PNG).Scale(icon_width, icon_height)
        open_camera_icon_image = wx.Image(open_camera_icon_path, wx.BITMAP_TYPE_PNG).Scale(icon_width, icon_height)
        rtsp_icon_image = wx.Image(rtsp_icon_path, wx.BITMAP_TYPE_PNG).Scale(icon_width, icon_height)
        alert_icon_image = wx.Image(alert_icon_path, wx.BITMAP_TYPE_PNG).Scale(icon_width, icon_height)

        browse_btn = wx.BitmapButton(panel, wx.ID_ANY, bitmap=wx.Bitmap(browse_icon_image), pos=(590, 247),
                                     size=(icon_chieudai, icon_chieurong))

        browse_btn.Bind(wx.EVT_BUTTON, self.on_open_browser)

        get_heatmap_btn = wx.BitmapButton(
            panel, wx.ID_ANY, bitmap=wx.Bitmap(heatmap_icon_image), pos=(85, 75), size=(icon_width, icon_height))
        get_heatmap_btn.Bind(wx.EVT_BUTTON, self.on_get_heatmap_analysis)

        open_heatmap_btn = wx.BitmapButton(
            panel, wx.ID_ANY, bitmap=wx.Bitmap(open_heatmap_icon_image), pos=(245, 75), size=(icon_width, icon_height))
        open_heatmap_btn.Bind(wx.EVT_BUTTON, self.on_open_heatmap)

        get_report_btn = wx.BitmapButton(
            panel, wx.ID_ANY, bitmap=wx.Bitmap(get_report_icon_image), pos=(390, 75), size=(icon_width, icon_height))
        get_report_btn.Bind(wx.EVT_BUTTON, self.on_get_report_analysis)

        open_excel_btn = wx.BitmapButton(
            panel, wx.ID_ANY, bitmap=wx.Bitmap(open_excel_icon_image), pos=(530, 75), size=(icon_width, icon_height))
        open_excel_btn.Bind(wx.EVT_BUTTON, self.on_open_excel)

        open_camera_btn = wx.BitmapButton(
            panel, wx.ID_ANY, bitmap=wx.Bitmap(open_camera_icon_image), pos=(170, 170), size=(icon_width, icon_height))
        open_camera_btn.Bind(wx.EVT_BUTTON, self.on_open_camera)

        rtsp_btn = wx.BitmapButton(
            panel, wx.ID_ANY, bitmap=wx.Bitmap(rtsp_icon_image), pos=(315, 170), size=(icon_width, icon_height))
        rtsp_btn.Bind(wx.EVT_BUTTON, self.on_rtsp)

        alert_btn = wx.BitmapButton(
            panel, wx.ID_ANY, bitmap=wx.Bitmap(alert_icon_image), pos=(460, 170), size=(icon_width, icon_height))
        alert_btn.Bind(wx.EVT_BUTTON, self.on_alert)

        self.video_path_tc = wx.TextCtrl(panel, size=(520, 25), pos=(40, 250))

        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT, size=(520, 200), pos=(40, 280))

        self.list.InsertColumn(0, 'Khu vực', wx.LIST_FORMAT_CENTER, width=80, )
        self.list.InsertColumn(1, 'Thời gian', wx.LIST_FORMAT_CENTER, 80)
        self.list.InsertColumn(2, 'Trung bình người / frame',
                               wx.LIST_FORMAT_CENTER, 160)
        self.list.InsertColumn(3, 'Tổng frame', wx.LIST_FORMAT_CENTER, 100)
        self.list.InsertColumn(4, 'Tổng người', wx.LIST_FORMAT_CENTER, 100)

        self.reset_list()

        self.Centre()
        self.Show()

    def on_alert(self, event):
        image_path = "data/alert.png"

        try:
            dialog = AlertDialog(self, "Alert Image", image_path)
            dialog.ShowModal()
        except Exception as e:
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def on_rtsp(self, event):
        rtsp_dialog = RTSPDialog(self, "Enter RTSP Link")
        result = rtsp_dialog.ShowModal()

        if result == wx.ID_OK:
            rtsp_link = rtsp_dialog.rtsp_text.GetValue()
            if rtsp_link:
                print(f"Entered RTSP Link: {rtsp_link}")
                runDetech(rtsp_link)

        rtsp_dialog.Destroy()

    def on_open_browser(self, event):
        openFileDialog = wx.FileDialog(
            self, "Open", "", "", "Python files (*.mp4)|*.mp4", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        self.video_path_tc.SetLabel(path)
        openFileDialog.Destroy()

    def on_get_heatmap_analysis(self, event):
        videoPath = self.video_path_tc.GetLabel()
        if self.video_path_tc.GetLabel() != '':
            progress_dialog = AnalystDialog(self, "Start progress...", "Please wait")
            runHeatmap(videoPath, progress_dialog=progress_dialog)

    def on_open_heatmap(self, event):
        file_path = path.relpath("data/output_heatmap_video.mp4")
        startfile(file_path)

    def on_get_report_analysis(self, event):
        result_analyst = []
        if self.video_path_tc.GetLabel() != '':
            progress_dialog = AnalystDialog(
                self, "Start progress...", "Please wait")
            runApplication(progress_dialog=progress_dialog,
                           video_path=self.video_path_tc.GetValue().replace("\\", "/"))
            try:
                self.list.DeleteAllItems()
                self.reset_list()
                with open("data/result_analyst.json", 'r') as openfile:
                    result_analyst = json.load(openfile)
                    for index, area in enumerate(result_analyst):
                        self.list.InsertItem(index, "-")
                        for i, rs in enumerate(area):
                            self.list.SetItem(index, i, str(rs))
            except IOError:
                result_analyst = []

    def on_open_excel(self, event):
        file_path = path.relpath("data/analyst.xlsx")
        startfile(file_path)

    def on_open_camera(self, event):
        runDetech(0)
        print('open camera')

    def reset_list(self):
        self.list.InsertItem(0, "-")
        self.list.SetItem(0, 1, "-")
        self.list.SetItem(0, 2, "-")
        self.list.SetItem(0, 3, "-")
        self.list.SetItem(0, 4, "-")


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
