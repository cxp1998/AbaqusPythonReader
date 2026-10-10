using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;
using PythonReader.Properties;

namespace PythonReader
{
	// Token: 0x02000004 RID: 4
	public class FormReader : Form
	{
		// Token: 0x0600002B RID: 43 RVA: 0x00002320 File Offset: 0x00000520
		protected override void Dispose(bool disposing)
		{
			if (disposing && this.components != null)
			{
				this.components.Dispose();
			}
			base.Dispose(disposing);
		}

		// Token: 0x0600002C RID: 44 RVA: 0x00002340 File Offset: 0x00000540
		private void InitializeComponent()
		{
			this.components = new Container();
			ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(FormReader));
			this.TSMenuItem = new ContextMenuStrip(this.components);
			this.TSMenuItemTextBrowser = new ToolStripMenuItem();
			this.TSMenuItemSaveAs = new ToolStripMenuItem();
			this.toolStripSeparator10 = new ToolStripSeparator();
			this.TSMenuItemCopy = new ToolStripMenuItem();
			this.TSMenuItemCMD = new ToolStripMenuItem();
			this.TSMenuItemCMDWordStyle = new ToolStripMenuItem();
			this.颜色ToolStripMenuItem = new ToolStripMenuItem();
			this.TSMenuItemCMDFontColor = new ToolStripMenuItem();
			this.toolStripSeparator4 = new ToolStripSeparator();
			this.TSMenuItemCMDBackColor = new ToolStripMenuItem();
			this.TSMenuItemCMDBorderColor = new ToolStripMenuItem();
			this.toolStripSeparator11 = new ToolStripSeparator();
			this.TSMenuItemCMDNewLine = new ToolStripMenuItem();
			this.TSMenuItemCMDScrollAuto = new ToolStripMenuItem();
			this.TSMenuItemCMDHighlightLastWords = new ToolStripMenuItem();
			this.toolStripSeparator8 = new ToolStripSeparator();
			this.TSMenuItemWinHide = new ToolStripMenuItem();
			this.TSMenuItemWinStyle = new ToolStripMenuItem();
			this.TSMenuItemWinStyleTopMost = new ToolStripMenuItem();
			this.toolStripSeparator12 = new ToolStripSeparator();
			this.TSMenuItemWinStyleNoShowInTaskBar = new ToolStripMenuItem();
			this.TSMenuItemWinStyleRightButtonDrag = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity0 = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity10 = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity20 = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity30 = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity40 = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity50 = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity60 = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity70 = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity80 = new ToolStripMenuItem();
			this.TSMenuItemWinStyleOpacity90 = new ToolStripMenuItem();
			this.toolStripSeparator1 = new ToolStripSeparator();
			this.TSMenuItemWinStyleWinStyleFrameNone = new ToolStripMenuItem();
			this.TSMenuItemWinStyleWinStyleFrameSizable = new ToolStripMenuItem();
			this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow = new ToolStripMenuItem();
			this.toolStripSeparator9 = new ToolStripSeparator();
			this.TSMenuItemOtherFunction = new ToolStripMenuItem();
			this.TSMenuItemOtherFunctionHelp = new ToolStripMenuItem();
			this.toolStripSeparator6 = new ToolStripSeparator();
			this.TSMenuItemOtherFunctionCheckUpdate = new ToolStripMenuItem();
			this.TSMenuItemOtherFunctionAbout = new ToolStripMenuItem();
			this.toolStripSeparator13 = new ToolStripSeparator();
			this.TSMenuItemQuit = new ToolStripMenuItem();
			this.toolStripSeparator2 = new ToolStripSeparator();
			this.timerOpenfile = new Timer(this.components);
			this.notifyIcon = new NotifyIcon(this.components);
			this.IconMenuItem = new ContextMenuStrip(this.components);
			this.IconMenuItemShowWin = new ToolStripMenuItem();
			this.toolStripSeparator7 = new ToolStripSeparator();
			this.IconMenuItemResetWinform = new ToolStripMenuItem();
			this.toolStripSeparator3 = new ToolStripSeparator();
			this.IconMenuItemGoogleGroup = new ToolStripMenuItem();
			this.IconMenuItemCheckUpdate = new ToolStripMenuItem();
			this.IconMenuItemAbout = new ToolStripMenuItem();
			this.toolStripSeparator5 = new ToolStripSeparator();
			this.IconMenuItemIconQuit = new ToolStripMenuItem();
			this.RichTextBoxPython = new RichTextBox();
			this.TSMenuItem.SuspendLayout();
			this.IconMenuItem.SuspendLayout();
			base.SuspendLayout();
			this.TSMenuItem.Items.AddRange(new ToolStripItem[]
			{
				this.TSMenuItemTextBrowser, this.TSMenuItemSaveAs, this.toolStripSeparator10, this.TSMenuItemCopy, this.TSMenuItemCMD, this.toolStripSeparator8, this.TSMenuItemWinHide, this.TSMenuItemWinStyle, this.toolStripSeparator9, this.TSMenuItemOtherFunction,
				this.toolStripSeparator13, this.TSMenuItemQuit
			});
			this.TSMenuItem.Name = "contextMenuStrip";
			this.TSMenuItem.Size = new Size(217, 204);
			this.TSMenuItem.Opening += new CancelEventHandler(this.TSMenuItem_Opening);
			this.TSMenuItemTextBrowser.Name = "TSMenuItemTextBrowser";
			this.TSMenuItemTextBrowser.ShortcutKeys = (Keys)131138;
			this.TSMenuItemTextBrowser.Size = new Size(216, 22);
			this.TSMenuItemTextBrowser.Text = "浏览(&B)...";
			this.TSMenuItemTextBrowser.Click += new EventHandler(this.IconMenuItemTextBrowser_Click);
			this.TSMenuItemSaveAs.Name = "TSMenuItemSaveAs";
			this.TSMenuItemSaveAs.ShortcutKeys = (Keys)131155;
			this.TSMenuItemSaveAs.Size = new Size(216, 22);
			this.TSMenuItemSaveAs.Text = "另存命令流为(&S)...";
			this.TSMenuItemSaveAs.Click += new EventHandler(this.TSMenuItemSaveAs_Click);
			this.toolStripSeparator10.Name = "toolStripSeparator10";
			this.toolStripSeparator10.Size = new Size(213, 6);
			this.TSMenuItemCopy.Name = "TSMenuItemCopy";
			this.TSMenuItemCopy.ShortcutKeys = (Keys)131139;
			this.TSMenuItemCopy.Size = new Size(216, 22);
			this.TSMenuItemCopy.Text = "复制(&C)";
			this.TSMenuItemCopy.Click += new EventHandler(this.TSMenuItemCopy_Click);
			this.TSMenuItemCMD.DropDownItems.AddRange(new ToolStripItem[] { this.TSMenuItemCMDWordStyle, this.颜色ToolStripMenuItem, this.toolStripSeparator11, this.TSMenuItemCMDNewLine, this.TSMenuItemCMDScrollAuto, this.TSMenuItemCMDHighlightLastWords });
			this.TSMenuItemCMD.Name = "TSMenuItemCMD";
			this.TSMenuItemCMD.Size = new Size(216, 22);
			this.TSMenuItemCMD.Text = "命令流样式";
			this.TSMenuItemCMDWordStyle.Name = "TSMenuItemCMDWordStyle";
			this.TSMenuItemCMDWordStyle.Size = new Size(213, 22);
			this.TSMenuItemCMDWordStyle.Text = "字体(&W)...";
			this.TSMenuItemCMDWordStyle.Click += new EventHandler(this.TSMenuItemCMDWordStyle_Click);
			this.颜色ToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { this.TSMenuItemCMDFontColor, this.toolStripSeparator4, this.TSMenuItemCMDBackColor, this.TSMenuItemCMDBorderColor });
			this.颜色ToolStripMenuItem.Name = "颜色ToolStripMenuItem";
			this.颜色ToolStripMenuItem.Size = new Size(213, 22);
			this.颜色ToolStripMenuItem.Text = "颜色";
			this.TSMenuItemCMDFontColor.Name = "TSMenuItemCMDFontColor";
			this.TSMenuItemCMDFontColor.Size = new Size(133, 22);
			this.TSMenuItemCMDFontColor.Text = "字体颜色...";
			this.TSMenuItemCMDFontColor.Click += new EventHandler(this.TSMenuItemCMDFontColor_Click);
			this.toolStripSeparator4.Name = "toolStripSeparator4";
			this.toolStripSeparator4.Size = new Size(130, 6);
			this.TSMenuItemCMDBackColor.Name = "TSMenuItemCMDBackColor";
			this.TSMenuItemCMDBackColor.Size = new Size(133, 22);
			this.TSMenuItemCMDBackColor.Text = "背景颜色...";
			this.TSMenuItemCMDBackColor.Click += new EventHandler(this.TSMenuItemCMDBackColor_Click);
			this.TSMenuItemCMDBorderColor.Name = "TSMenuItemCMDBorderColor";
			this.TSMenuItemCMDBorderColor.Size = new Size(133, 22);
			this.TSMenuItemCMDBorderColor.Text = "边框颜色...";
			this.TSMenuItemCMDBorderColor.Click += new EventHandler(this.TSMenuItemCMDBorderColor_Click);
			this.toolStripSeparator11.Name = "toolStripSeparator11";
			this.toolStripSeparator11.Size = new Size(210, 6);
			this.TSMenuItemCMDNewLine.Name = "TSMenuItemCMDNewLine";
			this.TSMenuItemCMDNewLine.Size = new Size(213, 22);
			this.TSMenuItemCMDNewLine.Text = "自动换行(&W)";
			this.TSMenuItemCMDNewLine.Click += new EventHandler(this.TSMenuItemCMDNewLine_Click);
			this.TSMenuItemCMDScrollAuto.Name = "TSMenuItemCMDScrollAuto";
			this.TSMenuItemCMDScrollAuto.Size = new Size(213, 22);
			this.TSMenuItemCMDScrollAuto.Text = "自动滚屏(&S)";
			this.TSMenuItemCMDScrollAuto.Click += new EventHandler(this.TSMenuItemCMDScrollAuto_Click);
			this.TSMenuItemCMDHighlightLastWords.Name = "TSMenuItemCMDHighlightLastWords";
			this.TSMenuItemCMDHighlightLastWords.Size = new Size(213, 22);
			this.TSMenuItemCMDHighlightLastWords.Text = "高亮显示最后一条语句(&H)";
			this.TSMenuItemCMDHighlightLastWords.Click += new EventHandler(this.TSMenuItemCMDHighlightLastWords_Click);
			this.toolStripSeparator8.Name = "toolStripSeparator8";
			this.toolStripSeparator8.Size = new Size(213, 6);
			this.TSMenuItemWinHide.Name = "TSMenuItemWinHide";
			this.TSMenuItemWinHide.ShortcutKeys = (Keys)131140;
			this.TSMenuItemWinHide.Size = new Size(216, 22);
			this.TSMenuItemWinHide.Text = "最小化到托盘(&D)";
			this.TSMenuItemWinHide.Click += new EventHandler(this.TSMenuItemWinHide_Click);
			this.TSMenuItemWinStyle.DropDownItems.AddRange(new ToolStripItem[] { this.TSMenuItemWinStyleTopMost, this.toolStripSeparator12, this.TSMenuItemWinStyleNoShowInTaskBar, this.TSMenuItemWinStyleRightButtonDrag, this.TSMenuItemWinStyleOpacity, this.toolStripSeparator1, this.TSMenuItemWinStyleWinStyleFrameNone, this.TSMenuItemWinStyleWinStyleFrameSizable, this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow });
			this.TSMenuItemWinStyle.Name = "TSMenuItemWinStyle";
			this.TSMenuItemWinStyle.Size = new Size(216, 22);
			this.TSMenuItemWinStyle.Text = "窗口样式";
			this.TSMenuItemWinStyleTopMost.Name = "TSMenuItemWinStyleTopMost";
			this.TSMenuItemWinStyleTopMost.ShortcutKeys = (Keys)131156;
			this.TSMenuItemWinStyleTopMost.Size = new Size(220, 22);
			this.TSMenuItemWinStyleTopMost.Text = "窗口置前(&T)";
			this.TSMenuItemWinStyleTopMost.Click += new EventHandler(this.TSMenuItemWinStyleTopMost_Click);
			this.toolStripSeparator12.Name = "toolStripSeparator12";
			this.toolStripSeparator12.Size = new Size(217, 6);
			this.TSMenuItemWinStyleNoShowInTaskBar.Name = "TSMenuItemWinStyleNoShowInTaskBar";
			this.TSMenuItemWinStyleNoShowInTaskBar.Size = new Size(220, 22);
			this.TSMenuItemWinStyleNoShowInTaskBar.Text = "隐藏任务栏图标";
			this.TSMenuItemWinStyleNoShowInTaskBar.Click += new EventHandler(this.TSMenuItemWinStyleNoShowInTaskBar_Click);
			this.TSMenuItemWinStyleRightButtonDrag.Name = "TSMenuItemWinStyleRightButtonDrag";
			this.TSMenuItemWinStyleRightButtonDrag.Size = new Size(220, 22);
			this.TSMenuItemWinStyleRightButtonDrag.Text = "鼠标右键移动窗口";
			this.TSMenuItemWinStyleRightButtonDrag.Click += new EventHandler(this.TSMenuItemWinStyleRightButtonDrag_Click);
			this.TSMenuItemWinStyleOpacity.DropDownItems.AddRange(new ToolStripItem[] { this.TSMenuItemWinStyleOpacity0, this.TSMenuItemWinStyleOpacity10, this.TSMenuItemWinStyleOpacity20, this.TSMenuItemWinStyleOpacity30, this.TSMenuItemWinStyleOpacity40, this.TSMenuItemWinStyleOpacity50, this.TSMenuItemWinStyleOpacity60, this.TSMenuItemWinStyleOpacity70, this.TSMenuItemWinStyleOpacity80, this.TSMenuItemWinStyleOpacity90 });
			this.TSMenuItemWinStyleOpacity.Name = "TSMenuItemWinStyleOpacity";
			this.TSMenuItemWinStyleOpacity.Size = new Size(220, 22);
			this.TSMenuItemWinStyleOpacity.Text = "窗口当前透明度：";
			this.TSMenuItemWinStyleOpacity0.Name = "TSMenuItemWinStyleOpacity0";
			this.TSMenuItemWinStyleOpacity0.ShortcutKeys = (Keys)131120;
			this.TSMenuItemWinStyleOpacity0.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity0.Text = "  0%";
			this.TSMenuItemWinStyleOpacity0.Click += new EventHandler(this.TSMenuItemWinStyleOpacity0_Click);
			this.TSMenuItemWinStyleOpacity10.Name = "TSMenuItemWinStyleOpacity10";
			this.TSMenuItemWinStyleOpacity10.ShortcutKeys = (Keys)131121;
			this.TSMenuItemWinStyleOpacity10.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity10.Text = "10%";
			this.TSMenuItemWinStyleOpacity10.Click += new EventHandler(this.TSMenuItemWinStyleOpacity10_Click);
			this.TSMenuItemWinStyleOpacity20.Name = "TSMenuItemWinStyleOpacity20";
			this.TSMenuItemWinStyleOpacity20.ShortcutKeys = (Keys)131122;
			this.TSMenuItemWinStyleOpacity20.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity20.Text = "20%";
			this.TSMenuItemWinStyleOpacity20.Click += new EventHandler(this.TSMenuItemWinStyleOpacity20_Click);
			this.TSMenuItemWinStyleOpacity30.Name = "TSMenuItemWinStyleOpacity30";
			this.TSMenuItemWinStyleOpacity30.ShortcutKeys = (Keys)131123;
			this.TSMenuItemWinStyleOpacity30.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity30.Text = "30%";
			this.TSMenuItemWinStyleOpacity30.Click += new EventHandler(this.TSMenuItemWinStyleOpacity30_Click);
			this.TSMenuItemWinStyleOpacity40.Name = "TSMenuItemWinStyleOpacity40";
			this.TSMenuItemWinStyleOpacity40.ShortcutKeys = (Keys)131124;
			this.TSMenuItemWinStyleOpacity40.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity40.Text = "40%";
			this.TSMenuItemWinStyleOpacity40.Click += new EventHandler(this.TSMenuItemWinStyleOpacity40_Click);
			this.TSMenuItemWinStyleOpacity50.Name = "TSMenuItemWinStyleOpacity50";
			this.TSMenuItemWinStyleOpacity50.ShortcutKeys = (Keys)131125;
			this.TSMenuItemWinStyleOpacity50.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity50.Text = "50%";
			this.TSMenuItemWinStyleOpacity50.Click += new EventHandler(this.TSMenuItemWinStyleOpacity50_Click);
			this.TSMenuItemWinStyleOpacity60.Name = "TSMenuItemWinStyleOpacity60";
			this.TSMenuItemWinStyleOpacity60.ShortcutKeys = (Keys)131126;
			this.TSMenuItemWinStyleOpacity60.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity60.Text = "60%";
			this.TSMenuItemWinStyleOpacity60.Click += new EventHandler(this.TSMenuItemWinStyleOpacity60_Click);
			this.TSMenuItemWinStyleOpacity70.Name = "TSMenuItemWinStyleOpacity70";
			this.TSMenuItemWinStyleOpacity70.ShortcutKeys = (Keys)131127;
			this.TSMenuItemWinStyleOpacity70.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity70.Text = "70%";
			this.TSMenuItemWinStyleOpacity70.Click += new EventHandler(this.TSMenuItemWinStyleOpacity70_Click);
			this.TSMenuItemWinStyleOpacity80.Name = "TSMenuItemWinStyleOpacity80";
			this.TSMenuItemWinStyleOpacity80.ShortcutKeys = (Keys)131128;
			this.TSMenuItemWinStyleOpacity80.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity80.Text = "80%";
			this.TSMenuItemWinStyleOpacity80.Click += new EventHandler(this.TSMenuItemWinStyleOpacity80_Click);
			this.TSMenuItemWinStyleOpacity90.Name = "TSMenuItemWinStyleOpacity90";
			this.TSMenuItemWinStyleOpacity90.ShortcutKeys = (Keys)131129;
			this.TSMenuItemWinStyleOpacity90.Size = new Size(146, 22);
			this.TSMenuItemWinStyleOpacity90.Text = "90%";
			this.TSMenuItemWinStyleOpacity90.Click += new EventHandler(this.TSMenuItemWinStyleOpacity90_Click);
			this.toolStripSeparator1.Name = "toolStripSeparator1";
			this.toolStripSeparator1.Size = new Size(217, 6);
			this.TSMenuItemWinStyleWinStyleFrameNone.Name = "TSMenuItemWinStyleWinStyleFrameNone";
			this.TSMenuItemWinStyleWinStyleFrameNone.Size = new Size(220, 22);
			this.TSMenuItemWinStyleWinStyleFrameNone.Text = "无边框";
			this.TSMenuItemWinStyleWinStyleFrameNone.Click += new EventHandler(this.TSMenuItemWinStyleWinStyleFrameNone_Click);
			this.TSMenuItemWinStyleWinStyleFrameSizable.Name = "TSMenuItemWinStyleWinStyleFrameSizable";
			this.TSMenuItemWinStyleWinStyleFrameSizable.Size = new Size(220, 22);
			this.TSMenuItemWinStyleWinStyleFrameSizable.Text = "可调整大小的边框";
			this.TSMenuItemWinStyleWinStyleFrameSizable.Click += new EventHandler(this.TSMenuItemWinStyleWinStyleFrameSizable_Click);
			this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow.Name = "TSMenuItemWinStyleWinStyleFrameSizableToolWindow";
			this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow.Size = new Size(220, 22);
			this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow.Text = "可调整大小的工具窗口边框";
			this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow.Click += new EventHandler(this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow_Click);
			this.toolStripSeparator9.Name = "toolStripSeparator9";
			this.toolStripSeparator9.Size = new Size(213, 6);
			this.TSMenuItemOtherFunction.DropDownItems.AddRange(new ToolStripItem[] { this.TSMenuItemOtherFunctionHelp, this.toolStripSeparator6, this.TSMenuItemOtherFunctionCheckUpdate, this.TSMenuItemOtherFunctionAbout });
			this.TSMenuItemOtherFunction.Name = "TSMenuItemOtherFunction";
			this.TSMenuItemOtherFunction.Size = new Size(216, 22);
			this.TSMenuItemOtherFunction.Text = "其他功能";
			this.TSMenuItemOtherFunctionHelp.Name = "TSMenuItemOtherFunctionHelp";
			this.TSMenuItemOtherFunctionHelp.ShortcutKeys = (Keys)112;
			this.TSMenuItemOtherFunctionHelp.Size = new Size(165, 22);
			this.TSMenuItemOtherFunctionHelp.Text = "打开帮助...";
			this.TSMenuItemOtherFunctionHelp.Click += new EventHandler(this.TSMenuItemOtherFunctionHelp_Click);
			this.toolStripSeparator6.Name = "toolStripSeparator6";
			this.toolStripSeparator6.Size = new Size(162, 6);
			this.TSMenuItemOtherFunctionCheckUpdate.Name = "TSMenuItemOtherFunctionCheckUpdate";
			this.TSMenuItemOtherFunctionCheckUpdate.Size = new Size(165, 22);
			this.TSMenuItemOtherFunctionCheckUpdate.Text = "检查更新...";
			this.TSMenuItemOtherFunctionCheckUpdate.Click += new EventHandler(this.TSMenuItemOtherFunctionCheckUpdate_Click);
			this.TSMenuItemOtherFunctionAbout.Name = "TSMenuItemOtherFunctionAbout";
			this.TSMenuItemOtherFunctionAbout.ShortcutKeys = (Keys)262209;
			this.TSMenuItemOtherFunctionAbout.Size = new Size(165, 22);
			this.TSMenuItemOtherFunctionAbout.Text = "关于(&A)...";
			this.TSMenuItemOtherFunctionAbout.Click += new EventHandler(this.TSMenuItemOtherFunctionAbout_Click);
			this.toolStripSeparator13.Name = "toolStripSeparator13";
			this.toolStripSeparator13.Size = new Size(213, 6);
			this.TSMenuItemQuit.Name = "TSMenuItemQuit";
			this.TSMenuItemQuit.ShortcutKeys = (Keys)262259;
			this.TSMenuItemQuit.Size = new Size(216, 22);
			this.TSMenuItemQuit.Text = "退出程序(&Q)";
			this.TSMenuItemQuit.Click += new EventHandler(this.TSMenuItemQuit_Click);
			this.toolStripSeparator2.Name = "toolStripSeparator2";
			this.toolStripSeparator2.Size = new Size(6, 6);
			this.timerOpenfile.Enabled = true;
			this.timerOpenfile.Tick += new EventHandler(this.timerOpenfile_Tick);
			this.notifyIcon.BalloonTipIcon = ToolTipIcon.Info;
			this.notifyIcon.BalloonTipTitle = "ABAQUS_PythonReader";
			this.notifyIcon.ContextMenuStrip = this.IconMenuItem;
			this.notifyIcon.Icon = (Icon)componentResourceManager.GetObject("notifyIcon.Icon");
			this.notifyIcon.Text = "ABAQUS_PythonReader";
			this.notifyIcon.Visible = true;
			this.notifyIcon.MouseDown += new MouseEventHandler(this.notifyIcon_MouseDown);
			this.IconMenuItem.Items.AddRange(new ToolStripItem[] { this.IconMenuItemShowWin, this.toolStripSeparator7, this.IconMenuItemResetWinform, this.toolStripSeparator3, this.IconMenuItemGoogleGroup, this.IconMenuItemCheckUpdate, this.IconMenuItemAbout, this.toolStripSeparator5, this.IconMenuItemIconQuit });
			this.IconMenuItem.Name = "contextMenuStripIcon";
			this.IconMenuItem.Size = new Size(182, 154);
			this.IconMenuItemShowWin.Checked = true;
			this.IconMenuItemShowWin.CheckState = CheckState.Checked;
			this.IconMenuItemShowWin.Font = new Font("宋体", 9f, FontStyle.Bold);
			this.IconMenuItemShowWin.Name = "IconMenuItemShowWin";
			this.IconMenuItemShowWin.Size = new Size(181, 22);
			this.IconMenuItemShowWin.Text = "显示窗口(&S)";
			this.IconMenuItemShowWin.Click += new EventHandler(this.IconMenuItemShowWin_Click);
			this.toolStripSeparator7.Name = "toolStripSeparator7";
			this.toolStripSeparator7.Size = new Size(178, 6);
			this.IconMenuItemResetWinform.Name = "IconMenuItemResetWinform";
			this.IconMenuItemResetWinform.Size = new Size(181, 22);
			this.IconMenuItemResetWinform.Text = "重置窗口(&R)";
			this.IconMenuItemResetWinform.Click += new EventHandler(this.IconMenuItemResetWinform_Click);
			this.toolStripSeparator3.Name = "toolStripSeparator3";
			this.toolStripSeparator3.Size = new Size(178, 6);
			this.IconMenuItemGoogleGroup.Name = "IconMenuItemGoogleGroup";
			this.IconMenuItemGoogleGroup.Size = new Size(181, 22);
			this.IconMenuItemGoogleGroup.Text = "Google讨论组(&G)...";
			this.IconMenuItemGoogleGroup.Visible = false;
			this.IconMenuItemGoogleGroup.Click += new EventHandler(this.IconMenuItemGoogleGroup_Click);
			this.IconMenuItemCheckUpdate.Name = "IconMenuItemCheckUpdate";
			this.IconMenuItemCheckUpdate.Size = new Size(181, 22);
			this.IconMenuItemCheckUpdate.Text = "检查更新...";
			this.IconMenuItemCheckUpdate.Click += new EventHandler(this.IconMenuItemCheckUpdate_Click);
			this.IconMenuItemAbout.Name = "IconMenuItemAbout";
			this.IconMenuItemAbout.Size = new Size(181, 22);
			this.IconMenuItemAbout.Text = "关于(&A)...";
			this.IconMenuItemAbout.Click += new EventHandler(this.IconMenuItemAbout_Click);
			this.toolStripSeparator5.Name = "toolStripSeparator5";
			this.toolStripSeparator5.Size = new Size(178, 6);
			this.IconMenuItemIconQuit.Name = "IconMenuItemIconQuit";
			this.IconMenuItemIconQuit.Size = new Size(181, 22);
			this.IconMenuItemIconQuit.Text = "退出程序(&Q)";
			this.IconMenuItemIconQuit.Click += new EventHandler(this.IconMenuItemIconQuit_Click);
			this.RichTextBoxPython.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
			this.RichTextBoxPython.BackColor = SystemColors.Window;
			this.RichTextBoxPython.BorderStyle = 0;
			this.RichTextBoxPython.ContextMenuStrip = this.TSMenuItem;
			this.RichTextBoxPython.HideSelection = false;
			this.RichTextBoxPython.Location = new Point(1, 1);
			this.RichTextBoxPython.Name = "RichTextBoxPython";
			this.RichTextBoxPython.ReadOnly = true;
			this.RichTextBoxPython.Size = new Size(638, 88);
			this.RichTextBoxPython.TabIndex = 4;
			this.RichTextBoxPython.Text = "";
			this.RichTextBoxPython.MouseUp += new MouseEventHandler(this.RichTextBoxPython_MouseUp);
			this.RichTextBoxPython.LinkClicked += new LinkClickedEventHandler(this.RichTextBoxPython_LinkClicked);
			this.RichTextBoxPython.SizeChanged += new EventHandler(this.RichTextBoxPython_SizeChanged);
			this.RichTextBoxPython.MouseMove += new MouseEventHandler(this.RichTextBoxPython_MouseMove);
			this.RichTextBoxPython.MouseDown += new MouseEventHandler(this.RichTextBoxPython_MouseDown);
			base.AutoScaleDimensions = new SizeF(6f, 12f);
			base.AutoScaleMode = AutoScaleMode.Font;
			this.BackColor = SystemColors.GradientInactiveCaption;
			base.ClientSize = new Size(640, 90);
			base.Controls.Add(this.RichTextBoxPython);
			base.FormBorderStyle = FormBorderStyle.None;
			base.Icon = (Icon)componentResourceManager.GetObject("$this.Icon");
			this.MinimumSize = new Size(200, 21);
			base.Name = "FormReader";
			base.StartPosition = FormStartPosition.CenterScreen;
			this.Text = "PythonReader";
			base.Load += new EventHandler(this.FormReader_Load);
			base.MouseDown += new MouseEventHandler(this.FormReader_MouseDown);
			base.FormClosing += new FormClosingEventHandler(this.FormReader_FormClosing);
			base.MouseMove += new MouseEventHandler(this.FormReader_MouseMove);
			this.TSMenuItem.ResumeLayout(false);
			this.IconMenuItem.ResumeLayout(false);
			base.ResumeLayout(false);
		}

		// Token: 0x0600002D RID: 45
		[DllImport("user32.dll")]
		[return: MarshalAs(UnmanagedType.Bool)]
		private static extern bool GetScrollInfo(IntPtr hwnd, int fnBar, ref FormReader.SCROLLINFO lpsi);

		// Token: 0x0600002E RID: 46
		[DllImport("user32.dll")]
		private static extern int SetScrollInfo(IntPtr hwnd, int fnBar, [In] ref FormReader.SCROLLINFO lpsi, bool fRedraw);

		// Token: 0x0600002F RID: 47
		[DllImport("User32.dll", CharSet = CharSet.Auto)]
		private static extern IntPtr SendMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);

		// Token: 0x06000030 RID: 48 RVA: 0x00003BB0 File Offset: 0x00001DB0
		public FormReader()
		{
			this.InitializeComponent();
		}

		// Token: 0x06000031 RID: 49 RVA: 0x00003C18 File Offset: 0x00001E18
		private void FormReader_Load(object sender, EventArgs e)
		{
			base.Hide();
			this.LoadSetting();
			base.Show();
		}

		// Token: 0x06000032 RID: 50 RVA: 0x00003C2C File Offset: 0x00001E2C
		private void SaveSetting()
		{
			Settings.Default.fOpacity = base.Opacity;
			Settings.Default.blTopmost = base.TopMost;
			Settings.Default.fWinfromLocationX = base.Location.X;
			Settings.Default.fWinfromLocationY = base.Location.Y;
			Settings.Default.fWinformSizeX = base.Width;
			Settings.Default.fWinformSizeY = base.Height;
			Settings.Default.blWordwrap = this.RichTextBoxPython.WordWrap;
			Settings.Default.blAutoScroll = this.blAutoScroll;
			Settings.Default.blHighlightNewCmd = this.blHighlightNewCmd;
			Settings.Default.blNoShowInTaskBar = this.TSMenuItemWinStyleNoShowInTaskBar.Checked;
			Settings.Default.blRightButtonDrag = this.TSMenuItemWinStyleRightButtonDrag.Checked;
			if (this.TSMenuItemWinStyleWinStyleFrameNone.Checked)
			{
				Settings.Default.fFormBorderStyle = 1;
			}
			if (this.TSMenuItemWinStyleWinStyleFrameSizable.Checked)
			{
				Settings.Default.fFormBorderStyle = 2;
			}
			if (this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow.Checked)
			{
				Settings.Default.fFormBorderStyle = 3;
			}
			Settings.Default.Save();
		}

		// Token: 0x06000033 RID: 51 RVA: 0x00003D5A File Offset: 0x00001F5A
		private void FormReader_FormClosing(object sender, FormClosingEventArgs e)
		{
			this.SaveSetting();
		}

		// Token: 0x06000034 RID: 52 RVA: 0x00003D64 File Offset: 0x00001F64
		private void MsgAbout()
		{
			MessageBox.Show(string.Concat(new string[]
			{
				"当前版本：",
				Resources.Version,
				"\n",
				Resources.UpdateData,
				"\n\n程序设计：焦博士 (ck436)\n联系方式：ck436@126.com\nQQ交流群：6547109\n\n功能说明：该程序能够适时检测abaqus.rpy文件的变化，以便查看CAE中UI操作对应的Python语句，为大家提供在ABAQUS PDE之外的又一Python学习辅助工具！\n\n操作提示：\n    1、程序第一次运行时需要指定abaqus.rpy的位置，以后运行会自动加载上一次设置；\n    2、在窗口中拖动右键可以移动窗口位置；\n    3、窗口无边框模式下把鼠标移动到窗口边缘可以拖动改变窗口大小；\n    4、通过右键打开帮助后直接退出程序再重启可以自动加载上次的abaqus.rpy文件。\n\n下步计划：增加命令流语法加亮功能。"
			}), "关于...", 0);
		}

		// Token: 0x06000035 RID: 53 RVA: 0x00003DB4 File Offset: 0x00001FB4
		private void ReadFile(string strFile)
		{
			try
			{
				this.fs = new FileStream(strFile, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
				this.reader = new StreamReader(this.fs, Encoding.Default);
				this.strCMD = "";
				this.fLastReadLineNoNew = 0;
				while (!this.reader.EndOfStream)
				{
					if (this.strCMD.Length == 0)
					{
						this.strCMD += this.reader.ReadLine();
						this.fLastReadLineNoNew++;
					}
					else
					{
						this.strCMD = this.strCMD + "\n" + this.reader.ReadLine();
						this.fLastReadLineNoNew++;
					}
				}
				this.reader.Close();
				this.fs.Close();
				if (this.blNewOpenFile)
				{
					this.fLastCMDLength = 0;
					this.RichTextBoxPython.Text = this.strCMD;
				}
				else if (this.strCMD.Length > this.fLastCMDLength)
				{
					this.RichTextBoxPython.AppendText(this.strCMD.Substring(this.fLastCMDLength, this.strCMD.Length - this.fLastCMDLength));
				}
				else
				{
					this.fLastCMDLength = 0;
					this.RichTextBoxPython.Text = this.strCMD;
				}
				this.fLastCMDLength = this.RichTextBoxPython.Text.Length;
			}
			catch
			{
				this.RichTextBoxPython.Text = "捕获到文件读取异常!";
			}
		}

		// Token: 0x06000036 RID: 54 RVA: 0x00003F4C File Offset: 0x0000214C
		private void SetFormBorderStyle(int style)
		{
			this.TSMenuItemWinStyleWinStyleFrameNone.Checked = false;
			this.TSMenuItemWinStyleWinStyleFrameSizable.Checked = false;
			this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow.Checked = false;
			if (style == 1)
			{
				base.FormBorderStyle = FormBorderStyle.None;
				this.TSMenuItemWinStyleWinStyleFrameNone.Checked = true;
				return;
			}
			if (style == 2)
			{
				base.FormBorderStyle = FormBorderStyle.Sizable;
				this.TSMenuItemWinStyleWinStyleFrameSizable.Checked = true;
				base.Icon = this.notifyIcon.Icon;
				return;
			}
			if (style == 3)
			{
				base.FormBorderStyle = FormBorderStyle.SizableToolWindow;
				this.TSMenuItemWinStyleWinStyleFrameSizableToolWindow.Checked = true;
			}
		}

		// Token: 0x06000037 RID: 55 RVA: 0x00003FD8 File Offset: 0x000021D8
		private void timerOpenfile_Tick(object sender, EventArgs e)
		{
			if (this.fFileDir != "")
			{
				this.filedir = new FileInfo(this.fFileDir);
				if (this.filedir.Exists)
				{
					if (File.GetLastWriteTime(this.filedir.FullName) != this.fDateTimeLastWrite || this.blNewOpenFile)
					{
						this.fLastRichTextBoxLength = this.RichTextBoxPython.Text.Length;
						if (this.blNewOpenFile)
						{
							this.fLastRichTextBoxLength = 0;
							this.fLastReadLineNoOld = 0;
							this.fLastCMDLength = 0;
						}
						this.ScrollRichTextBoxPython(3);
						this.ReadFile(this.fFileDir);
						this.fDateTimeLastWrite = File.GetLastWriteTime(this.filedir.FullName);
						if (this.blHighlightNewCmd)
						{
							if (this.fLastRichTextBoxLength != 0 && this.fLastReadLineNoNew > this.fLastReadLineNoOld)
							{
								this.fLastRichTextBoxLength++;
							}
							if (this.RichTextBoxPython.Text.Length > this.fLastRichTextBoxLength)
							{
								this.RichTextBoxPython.Select(this.fLastRichTextBoxLength, this.RichTextBoxPython.Text.Length - this.fLastRichTextBoxLength);
							}
							else if (this.RichTextBoxPython.Text.Length != this.fLastRichTextBoxLength)
							{
								this.RichTextBoxPython.SelectAll();
							}
						}
						this.fLastReadLineNoOld = this.fLastReadLineNoNew;
						if (this.blAutoScroll)
						{
							this.ScrollRichTextBoxPython(1);
						}
						else
						{
							this.ScrollRichTextBoxPython(2);
						}
						this.blNewOpenFile = false;
						return;
					}
				}
				else
				{
					this.RichTextBoxPython.Text = "文件:" + this.filedir.FullName + "不存在!";
				}
			}
		}

		// Token: 0x06000038 RID: 56 RVA: 0x00004184 File Offset: 0x00002384
		private void TSMenuItemCopy_Click(object sender, EventArgs e)
		{
			this.RichTextBoxPython.Copy();
		}

		// Token: 0x06000039 RID: 57 RVA: 0x00004194 File Offset: 0x00002394
		private void BrowserFile()
		{
			OpenFileDialog openFileDialog = new OpenFileDialog();
			openFileDialog.InitialDirectory = Environment.CurrentDirectory;
			openFileDialog.CheckFileExists = true;
			openFileDialog.Filter = "ABAQUS/CAE命令|abaqus.rpy|所有文件(*.*)|*.*";
			openFileDialog.Multiselect = false;
			if (openFileDialog.ShowDialog() == DialogResult.OK)
			{
				this.fFileDir = openFileDialog.FileName;
				this.Text = this.fFileDir.ToString() + " - PythonReader " + Resources.Version;
				this.blNewOpenFile = true;
				Settings.Default.strLastFileName = this.fFileDir.ToString();
				Settings.Default.Save();
			}
		}

		// Token: 0x0600003A RID: 58 RVA: 0x00004226 File Offset: 0x00002426
		private void IconMenuItemIconQuit_Click(object sender, EventArgs e)
		{
			base.Close();
		}

		// Token: 0x0600003B RID: 59 RVA: 0x0000422E File Offset: 0x0000242E
		private void IconMenuItemShowWin_Click(object sender, EventArgs e)
		{
			this.WinHide();
		}

		// Token: 0x0600003C RID: 60 RVA: 0x00004236 File Offset: 0x00002436
		private void notifyIcon_MouseDown(object sender, MouseEventArgs e)
		{
			if (e.Button == MouseButtons.Left)
			{
				this.WinHide();
			}
		}

		// Token: 0x0600003D RID: 61 RVA: 0x0000424B File Offset: 0x0000244B
		private void IconMenuItemAbout_Click(object sender, EventArgs e)
		{
			this.MsgAbout();
		}

		// Token: 0x0600003E RID: 62 RVA: 0x00004253 File Offset: 0x00002453
		private void TSMenuItemWinStyleWinStyleFrameSizableToolWindow_Click(object sender, EventArgs e)
		{
			this.SetFormBorderStyle(3);
		}

		// Token: 0x0600003F RID: 63 RVA: 0x0000425C File Offset: 0x0000245C
		private void TSMenuItemWinStyleWinStyleFrameNone_Click(object sender, EventArgs e)
		{
			this.SetFormBorderStyle(1);
		}

		// Token: 0x06000040 RID: 64 RVA: 0x00004265 File Offset: 0x00002465
		private void TSMenuItemWinStyleWinStyleFrameSizable_Click(object sender, EventArgs e)
		{
			this.SetFormBorderStyle(2);
		}

		// Token: 0x06000041 RID: 65 RVA: 0x0000426E File Offset: 0x0000246E
		private void TSMenuItemQuit_Click(object sender, EventArgs e)
		{
			base.Close();
		}

		// Token: 0x06000042 RID: 66 RVA: 0x00004276 File Offset: 0x00002476
		private void TSMenuItemWinHide_Click(object sender, EventArgs e)
		{
			this.WinHide();
		}

		// Token: 0x06000043 RID: 67 RVA: 0x00004280 File Offset: 0x00002480
		private void WinHide()
		{
			if (base.FormBorderStyle == FormBorderStyle.None)
			{
				if (base.Visible)
				{
					base.FormBorderStyle = FormBorderStyle.SizableToolWindow;
					base.WindowState = FormWindowState.Minimized;
					this.IconMenuItemShowWin.Checked = false;
					base.Visible = false;
					base.FormBorderStyle = FormBorderStyle.None;
					return;
				}
				base.Show();
				base.WindowState = FormWindowState.Normal;
				base.FormBorderStyle = FormBorderStyle.None;
				this.IconMenuItemShowWin.Checked = true;
				base.Visible = true;
				return;
			}
			else
			{
				if (base.Visible)
				{
					base.WindowState = FormWindowState.Minimized;
					this.IconMenuItemShowWin.Checked = false;
					base.Visible = false;
					return;
				}
				base.Show();
				base.WindowState = FormWindowState.Normal;
				this.IconMenuItemShowWin.Checked = true;
				base.Visible = true;
				return;
			}
		}

		// Token: 0x06000044 RID: 68 RVA: 0x00004331 File Offset: 0x00002531
		private void IconMenuItemGoogleGroup_Click(object sender, EventArgs e)
		{
			Process.Start(Resources.URLGoogleGroup);
		}

		// Token: 0x06000045 RID: 69 RVA: 0x0000433E File Offset: 0x0000253E
		private void IconMenuItemCheckUpdate_Click(object sender, EventArgs e)
		{
			Process.Start(Resources.URLUpdateCheck);
		}

		// Token: 0x06000046 RID: 70 RVA: 0x0000434B File Offset: 0x0000254B
		private void TSMenuItemCMDWordStyle_Click(object sender, EventArgs e)
		{
			this.SelectCMDStyle();
		}

		// Token: 0x06000047 RID: 71 RVA: 0x00004354 File Offset: 0x00002554
		private void SelectCMDStyle()
		{
			FontDialog fontDialog = new FontDialog();
			fontDialog.ShowColor = false;
			fontDialog.ShowApply = false;
			fontDialog.Font = Settings.Default.Font;
			if (fontDialog.ShowDialog() == DialogResult.OK)
			{
				this.RichTextBoxPython.Font = fontDialog.Font;
				this.RichTextBoxPython.ForeColor = fontDialog.Color;
				Settings.Default.Font = fontDialog.Font;
				Settings.Default.Save();
			}
			fontDialog.Dispose();
		}

		// Token: 0x06000048 RID: 72 RVA: 0x000043D0 File Offset: 0x000025D0
		private void TSMenuItemCMDNewLine_Click(object sender, EventArgs e)
		{
			this.TSMenuItemCMDNewLine.Checked = !this.RichTextBoxPython.WordWrap;
			this.RichTextBoxPython.WordWrap = this.TSMenuItemCMDNewLine.Checked;
			if (this.blAutoScroll)
			{
				this.ScrollRichTextBoxPython(1);
			}
		}

		// Token: 0x06000049 RID: 73 RVA: 0x00004410 File Offset: 0x00002610
		private void TSMenuItemCMDScrollAuto_Click(object sender, EventArgs e)
		{
			this.TSMenuItemCMDScrollAuto.Checked = !this.blAutoScroll;
			this.blAutoScroll = this.TSMenuItemCMDScrollAuto.Checked;
			if (this.TSMenuItemCMDScrollAuto.Checked)
			{
				this.ScrollRichTextBoxPython(1);
			}
		}

		// Token: 0x0600004A RID: 74 RVA: 0x0000444C File Offset: 0x0000264C
		private void TSMenuItemCMDHighlightLastWords_Click(object sender, EventArgs e)
		{
			this.TSMenuItemCMDHighlightLastWords.Checked = !this.blHighlightNewCmd;
			this.blHighlightNewCmd = this.TSMenuItemCMDHighlightLastWords.Checked;
			if (!this.blHighlightNewCmd)
			{
				this.RichTextBoxPython.Select(this.RichTextBoxPython.Text.Length, 0);
			}
		}

		// Token: 0x0600004B RID: 75 RVA: 0x000044A2 File Offset: 0x000026A2
		private void TSMenuItemWinStyleTopMost_Click(object sender, EventArgs e)
		{
			this.TSMenuItemWinStyleTopMost.Checked = !base.TopMost;
			base.TopMost = this.TSMenuItemWinStyleTopMost.Checked;
		}

		// Token: 0x0600004C RID: 76 RVA: 0x000044C9 File Offset: 0x000026C9
		private void TSMenuItemOtherFunctionCheckUpdate_Click(object sender, EventArgs e)
		{
			Process.Start(Resources.URLUpdateCheck);
		}

		// Token: 0x0600004D RID: 77 RVA: 0x000044D6 File Offset: 0x000026D6
		private void TSMenuItemOtherFunctionAbout_Click(object sender, EventArgs e)
		{
			this.MsgAbout();
		}

		// Token: 0x0600004E RID: 78 RVA: 0x000044E0 File Offset: 0x000026E0
		private void LoadSetting()
		{
			this.Text = Settings.Default.strLastFileName + " - PythonReader " + Resources.Version;
			base.TopMost = Settings.Default.blTopmost;
			this.TSMenuItemWinStyleTopMost.Checked = base.TopMost;
			this.SetFormBorderStyle(Settings.Default.fFormBorderStyle);
			this.RichTextBoxPython.WordWrap = Settings.Default.blWordwrap;
			this.TSMenuItemCMDNewLine.Checked = Settings.Default.blWordwrap;
			this.blAutoScroll = Settings.Default.blAutoScroll;
			this.TSMenuItemCMDScrollAuto.Checked = Settings.Default.blAutoScroll;
			this.blHighlightNewCmd = Settings.Default.blHighlightNewCmd;
			this.TSMenuItemCMDHighlightLastWords.Checked = this.blHighlightNewCmd;
			this.TSMenuItemWinStyleNoShowInTaskBar.Checked = Settings.Default.blNoShowInTaskBar;
			base.ShowInTaskbar = !this.TSMenuItemWinStyleNoShowInTaskBar.Checked;
			this.TSMenuItemWinStyleRightButtonDrag.Checked = Settings.Default.blRightButtonDrag;
			this.fFileDir = Settings.Default.strLastFileName;
			if (Settings.Default.blFirstRun)
			{
				Settings.Default.blFirstRun = false;
				Settings.Default.Save();
			}
			else
			{
				base.Location = new Point(Settings.Default.fWinfromLocationX, Settings.Default.fWinfromLocationY);
				base.Width = Settings.Default.fWinformSizeX;
				base.Height = Settings.Default.fWinformSizeY;
			}
			this.RichTextBoxPython.ForeColor = Settings.Default.FontColor;
			this.RichTextBoxPython.Font = Settings.Default.Font;
			this.RichTextBoxPython.BackColor = Settings.Default.BackColor;
			this.BackColor = Settings.Default.BorderColor;
		}

		// Token: 0x0600004F RID: 79 RVA: 0x000046AC File Offset: 0x000028AC
		private void TSMenuItem_Opening(object sender, CancelEventArgs e)
		{
			if (this.RichTextBoxPython.SelectedText != "")
			{
				this.TSMenuItemCopy.Enabled = true;
			}
			else
			{
				this.TSMenuItemCopy.Enabled = false;
			}
			double num = 100.0 - base.Opacity * 100.0;
			this.TSMenuItemWinStyleOpacity.Text = "窗口当前透明度：" + num.ToString() + "%";
		}

		// Token: 0x06000050 RID: 80 RVA: 0x00004726 File Offset: 0x00002926
		private void TSMenuItemWinStyleNoShowInTaskBar_Click(object sender, EventArgs e)
		{
			this.TSMenuItemWinStyleNoShowInTaskBar.Checked = !this.TSMenuItemWinStyleNoShowInTaskBar.Checked;
			base.ShowInTaskbar = !this.TSMenuItemWinStyleNoShowInTaskBar.Checked;
		}

		// Token: 0x06000051 RID: 81 RVA: 0x00004758 File Offset: 0x00002958
		private void RichTextBoxPython_MouseMove(object sender, MouseEventArgs e)
		{
			Point point;
			point = new Point(e.X, e.Y);
			point = base.PointToScreen(point);
			int num = 0;
			if ((point.X - this.frmLocationMouseOld.X > num || point.X - this.frmLocationMouseOld.X < -num || point.Y - this.frmLocationMouseOld.Y > num || point.Y - this.frmLocationMouseOld.Y < -num) && this.TSMenuItemWinStyleRightButtonDrag.Checked && e.Button == MouseButtons.Right)
			{
				this.Cursor = Cursors.SizeAll;
				this.RichTextBoxPython.ContextMenuStrip = null;
				base.Top += point.Y - this.frmLocationMouseOld.Y;
				base.Left += point.X - this.frmLocationMouseOld.X;
				this.frmLocationMouseOld = point;
			}
		}

		// Token: 0x06000052 RID: 82 RVA: 0x00004854 File Offset: 0x00002A54
		private void FormReader_MouseMove(object sender, MouseEventArgs e)
		{
			if (e.Button == MouseButtons.None)
			{
				if (e.X > base.Size.Width - 8 && e.Y > base.Size.Height - 8)
				{
					this.Cursor = Cursors.SizeNWSE;
					if (e.Button == MouseButtons.Left)
					{
						base.Size = new Size(this.frmSizeOld.X + e.X - this.frmLocationMouseOld.X, this.frmSizeOld.Y + e.Y - this.frmLocationMouseOld.Y);
					}
				}
				else if (e.X > base.Size.Width - 2)
				{
					this.Cursor = Cursors.SizeWE;
					if (e.Button == MouseButtons.Left)
					{
						base.Size = new Size(this.frmSizeOld.X + e.X - this.frmLocationMouseOld.X, this.frmSizeOld.Y);
					}
				}
				else if (e.Y > base.Size.Height - 2)
				{
					this.Cursor = Cursors.SizeNS;
					if (e.Button == MouseButtons.Left)
					{
						base.Size = new Size(this.frmSizeOld.X, this.frmSizeOld.Y + e.Y - this.frmLocationMouseOld.Y);
					}
				}
				else
				{
					this.Cursor = Cursors.Default;
				}
			}
			if (e.Button == MouseButtons.Left)
			{
				if (this.Cursor == Cursors.SizeNWSE)
				{
					base.Size = new Size(this.frmSizeOld.X + e.X - this.frmLocationMouseOld.X, this.frmSizeOld.Y + e.Y - this.frmLocationMouseOld.Y);
					return;
				}
				if (this.Cursor == Cursors.SizeWE)
				{
					base.Size = new Size(this.frmSizeOld.X + e.X - this.frmLocationMouseOld.X, this.frmSizeOld.Y);
					return;
				}
				if (this.Cursor == Cursors.SizeNS)
				{
					base.Size = new Size(this.frmSizeOld.X, this.frmSizeOld.Y + e.Y - this.frmLocationMouseOld.Y);
					return;
				}
				this.Cursor = Cursors.Default;
			}
		}

		// Token: 0x06000053 RID: 83 RVA: 0x00004AE0 File Offset: 0x00002CE0
		private void RichTextBoxPython_MouseUp(object sender, MouseEventArgs e)
		{
			if (e.Button == MouseButtons.Right)
			{
				this.RichTextBoxPython.Visible = false;
				this.RichTextBoxPython.Visible = true;
			}
			this.Cursor = Cursors.Default;
		}

		// Token: 0x06000054 RID: 84 RVA: 0x00004B14 File Offset: 0x00002D14
		private void RichTextBoxPython_MouseDown(object sender, MouseEventArgs e)
		{
			if (this.TSMenuItemWinStyleRightButtonDrag.Checked)
			{
				this.frmLocationMouseOld = new Point(e.X, e.Y);
				this.frmLocationMouseOld = base.PointToScreen(this.frmLocationMouseOld);
			}
			this.RichTextBoxPython.ContextMenuStrip = this.TSMenuItem;
		}

		// Token: 0x06000055 RID: 85 RVA: 0x00004B68 File Offset: 0x00002D68
		private void FormReader_MouseDown(object sender, MouseEventArgs e)
		{
			this.frmLocationMouseOld = new Point(e.X, e.Y);
			this.frmSizeOld = new Point(base.Size.Width, base.Size.Height);
		}

		// Token: 0x06000056 RID: 86 RVA: 0x00004BB3 File Offset: 0x00002DB3
		private void TSMenuItemWinStyleRightButtonDrag_Click(object sender, EventArgs e)
		{
			this.TSMenuItemWinStyleRightButtonDrag.Checked = !this.TSMenuItemWinStyleRightButtonDrag.Checked;
		}

		// Token: 0x06000057 RID: 87 RVA: 0x00004BCE File Offset: 0x00002DCE
		private void IconMenuItemTextBrowser_Click(object sender, EventArgs e)
		{
			this.BrowserFile();
		}

		// Token: 0x06000058 RID: 88 RVA: 0x00004BD6 File Offset: 0x00002DD6
		private void RichTextBoxPython_LinkClicked(object sender, LinkClickedEventArgs e)
		{
			Process.Start(e.LinkText);
		}

		// Token: 0x06000059 RID: 89 RVA: 0x00004BE4 File Offset: 0x00002DE4
		private void ScrollRichTextBoxPython(int blScroll2Buttom)
		{
			IntPtr intPtr;
			intPtr = IntPtr.Zero;
			IntPtr handle = this.RichTextBoxPython.Handle;
			FormReader.SCROLLINFO scrollinfo = default(FormReader.SCROLLINFO);
			scrollinfo.cbSize = (uint)Marshal.SizeOf(scrollinfo);
			scrollinfo.fMask = 23U;
			FormReader.GetScrollInfo(handle, 1, ref scrollinfo);
			IntPtr intPtr2;
			if (blScroll2Buttom == 1)
			{
				intPtr2 = new IntPtr(7);
				FormReader.SendMessage(handle, 277U, intPtr2, intPtr);
				return;
			}
			if (blScroll2Buttom == 2)
			{
				scrollinfo.nPos = this.CurrentRichTextBoxPythonPos;
				FormReader.SetScrollInfo(handle, 1, ref scrollinfo, true);
				intPtr2 = new IntPtr(5 + 65536 * scrollinfo.nPos);
				FormReader.SendMessage(handle, 277U, intPtr2, intPtr);
				return;
			}
			if (blScroll2Buttom == 3)
			{
				this.CurrentRichTextBoxPythonPos = scrollinfo.nPos;
			}
		}

		// Token: 0x0600005A RID: 90 RVA: 0x00004C9F File Offset: 0x00002E9F
		private void RichTextBoxPython_SizeChanged(object sender, EventArgs e)
		{
			if (this.blIsAtButtom())
			{
				this.ScrollRichTextBoxPython(1);
			}
		}

		// Token: 0x0600005B RID: 91 RVA: 0x00004CB0 File Offset: 0x00002EB0
		private bool blIsAtButtom()
		{
			
			IntPtr handle = this.RichTextBoxPython.Handle;
			FormReader.SCROLLINFO scrollinfo = default(FormReader.SCROLLINFO);
			scrollinfo.cbSize = (uint)Marshal.SizeOf(scrollinfo);
			scrollinfo.fMask = 23U;
			FormReader.GetScrollInfo(handle, 1, ref scrollinfo);
			return scrollinfo.nPos >= scrollinfo.nMax - (int)scrollinfo.nPage - 20;
		}

		// Token: 0x0600005C RID: 92 RVA: 0x00004D1B File Offset: 0x00002F1B
		private void SetWinOpacity(double value)
		{
			base.Opacity = 1.0 - value / 100.0;
		}

		// Token: 0x0600005D RID: 93 RVA: 0x00004D38 File Offset: 0x00002F38
		private void TSMenuItemWinStyleOpacity0_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(0.0);
		}

		// Token: 0x0600005E RID: 94 RVA: 0x00004D49 File Offset: 0x00002F49
		private void TSMenuItemWinStyleOpacity10_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(10.0);
		}

		// Token: 0x0600005F RID: 95 RVA: 0x00004D5A File Offset: 0x00002F5A
		private void TSMenuItemWinStyleOpacity20_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(20.0);
		}

		// Token: 0x06000060 RID: 96 RVA: 0x00004D6B File Offset: 0x00002F6B
		private void TSMenuItemWinStyleOpacity30_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(30.0);
		}

		// Token: 0x06000061 RID: 97 RVA: 0x00004D7C File Offset: 0x00002F7C
		private void TSMenuItemWinStyleOpacity40_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(40.0);
		}

		// Token: 0x06000062 RID: 98 RVA: 0x00004D8D File Offset: 0x00002F8D
		private void TSMenuItemWinStyleOpacity50_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(50.0);
		}

		// Token: 0x06000063 RID: 99 RVA: 0x00004D9E File Offset: 0x00002F9E
		private void TSMenuItemWinStyleOpacity60_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(60.0);
		}

		// Token: 0x06000064 RID: 100 RVA: 0x00004DAF File Offset: 0x00002FAF
		private void TSMenuItemWinStyleOpacity70_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(70.0);
		}

		// Token: 0x06000065 RID: 101 RVA: 0x00004DC0 File Offset: 0x00002FC0
		private void TSMenuItemWinStyleOpacity80_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(80.0);
		}

		// Token: 0x06000066 RID: 102 RVA: 0x00004DD1 File Offset: 0x00002FD1
		private void TSMenuItemWinStyleOpacity90_Click(object sender, EventArgs e)
		{
			this.SetWinOpacity(90.0);
		}

		// Token: 0x06000067 RID: 103 RVA: 0x00004DE4 File Offset: 0x00002FE4
		private void IconMenuItemResetWinform_Click(object sender, EventArgs e)
		{
			base.Size = new Size(640, 90);
			base.Location = new Point((Screen.PrimaryScreen.WorkingArea.Width - base.Size.Width) / 2, (Screen.PrimaryScreen.WorkingArea.Height - base.Size.Height) / 2);
		}

		// Token: 0x06000068 RID: 104 RVA: 0x00004E54 File Offset: 0x00003054
		private void TSMenuItemOtherFunctionHelp_Click(object sender, EventArgs e)
		{
			this.fFileDir = this.strCurrentDirectory + "\\readme.txt";
			this.Text = this.fFileDir.ToString() + " - PythonReader " + Resources.Version;
		}

		// Token: 0x06000069 RID: 105 RVA: 0x00004E8C File Offset: 0x0000308C
		private void TSMenuItemSaveAs_Click(object sender, EventArgs e)
		{
			SaveFileDialog saveFileDialog = new SaveFileDialog();
			saveFileDialog.InitialDirectory = Environment.GetFolderPath(0);
			saveFileDialog.Title = "将命令流另存为：";
			saveFileDialog.AddExtension = true;
			saveFileDialog.Filter = "Python命令(*.py)|*.py|文本文件(*.txt)|*.txt|所有文件(*.*)|*.*";
			if (saveFileDialog.ShowDialog() == DialogResult.OK)
			{
				File.Copy(this.fFileDir, saveFileDialog.FileName, true);
			}
		}

		// Token: 0x0600006A RID: 106 RVA: 0x00004EE4 File Offset: 0x000030E4
		private void TSMenuItemCMDBackColor_Click(object sender, EventArgs e)
		{
			ColorDialog colorDialog = new ColorDialog();
			colorDialog.AllowFullOpen = true;
			colorDialog.FullOpen = true;
			colorDialog.Color = Settings.Default.BackColor;
			if (colorDialog.ShowDialog() != DialogResult.Cancel)
			{
				this.RichTextBoxPython.BackColor = colorDialog.Color;
				Settings.Default.BackColor = colorDialog.Color;
				Settings.Default.Save();
			}
		}

		// Token: 0x0600006B RID: 107 RVA: 0x00004F4C File Offset: 0x0000314C
		private void TSMenuItemCMDBorderColor_Click(object sender, EventArgs e)
		{
			ColorDialog colorDialog = new ColorDialog();
			colorDialog.AllowFullOpen = true;
			colorDialog.FullOpen = true;
			colorDialog.Color = Settings.Default.BorderColor;
			if (colorDialog.ShowDialog() != DialogResult.Cancel)
			{
				this.BackColor = colorDialog.Color;
				Settings.Default.BorderColor = colorDialog.Color;
				Settings.Default.Save();
			}
		}

		// Token: 0x0600006C RID: 108 RVA: 0x00004FAC File Offset: 0x000031AC
		private void TSMenuItemCMDFontColor_Click(object sender, EventArgs e)
		{
			ColorDialog colorDialog = new ColorDialog();
			colorDialog.AllowFullOpen = true;
			colorDialog.FullOpen = true;
			colorDialog.Color = Settings.Default.FontColor;
			if (colorDialog.ShowDialog() != DialogResult.Cancel)
			{
				this.RichTextBoxPython.ForeColor = colorDialog.Color;
				Settings.Default.FontColor = colorDialog.Color;
				Settings.Default.Save();
			}
		}

		// Token: 0x04000002 RID: 2
		private const int WM_VSCROLL = 277;

		// Token: 0x04000003 RID: 3
		private const int SB_LINEUP = 0;

		// Token: 0x04000004 RID: 4
		private const int SB_LINEDOWN = 1;

		// Token: 0x04000005 RID: 5
		private const int SB_THUMBPOSITION = 4;

		// Token: 0x04000006 RID: 6
		private const int SB_THUMBTRACK = 5;

		// Token: 0x04000007 RID: 7
		private const int SB_TOP = 6;

		// Token: 0x04000008 RID: 8
		private const int SB_BOTTOM = 7;

		// Token: 0x04000009 RID: 9
		private const int SB_ENDSCROLL = 8;

		// Token: 0x0400000A RID: 10
		private IContainer components;

		// Token: 0x0400000B RID: 11
		private Timer timerOpenfile;

		// Token: 0x0400000C RID: 12
		private ContextMenuStrip TSMenuItem;

		// Token: 0x0400000D RID: 13
		private ToolStripMenuItem TSMenuItemCopy;

		// Token: 0x0400000E RID: 14
		private NotifyIcon notifyIcon;

		// Token: 0x0400000F RID: 15
		private ContextMenuStrip IconMenuItem;

		// Token: 0x04000010 RID: 16
		private ToolStripMenuItem IconMenuItemShowWin;

		// Token: 0x04000011 RID: 17
		private ToolStripSeparator toolStripSeparator5;

		// Token: 0x04000012 RID: 18
		private ToolStripMenuItem IconMenuItemIconQuit;

		// Token: 0x04000013 RID: 19
		private ToolStripMenuItem TSMenuItemTextBrowser;

		// Token: 0x04000014 RID: 20
		private ToolStripSeparator toolStripSeparator7;

		// Token: 0x04000015 RID: 21
		private ToolStripMenuItem IconMenuItemAbout;

		// Token: 0x04000016 RID: 22
		private ToolStripSeparator toolStripSeparator8;

		// Token: 0x04000017 RID: 23
		private ToolStripMenuItem TSMenuItemWinStyle;

		// Token: 0x04000018 RID: 24
		private ToolStripMenuItem TSMenuItemWinStyleWinStyleFrameSizable;

		// Token: 0x04000019 RID: 25
		private ToolStripMenuItem TSMenuItemWinStyleWinStyleFrameSizableToolWindow;

		// Token: 0x0400001A RID: 26
		private ToolStripMenuItem TSMenuItemWinStyleWinStyleFrameNone;

		// Token: 0x0400001B RID: 27
		private ToolStripSeparator toolStripSeparator9;

		// Token: 0x0400001C RID: 28
		private ToolStripMenuItem TSMenuItemQuit;

		// Token: 0x0400001D RID: 29
		private ToolStripMenuItem TSMenuItemWinHide;

		// Token: 0x0400001E RID: 30
		private ToolStripMenuItem IconMenuItemGoogleGroup;

		// Token: 0x0400001F RID: 31
		private ToolStripMenuItem IconMenuItemCheckUpdate;

		// Token: 0x04000020 RID: 32
		private ToolStripSeparator toolStripSeparator10;

		// Token: 0x04000021 RID: 33
		private ToolStripMenuItem TSMenuItemCMD;

		// Token: 0x04000022 RID: 34
		private ToolStripMenuItem TSMenuItemCMDWordStyle;

		// Token: 0x04000023 RID: 35
		private ToolStripSeparator toolStripSeparator11;

		// Token: 0x04000024 RID: 36
		private ToolStripMenuItem TSMenuItemCMDNewLine;

		// Token: 0x04000025 RID: 37
		private ToolStripMenuItem TSMenuItemCMDScrollAuto;

		// Token: 0x04000026 RID: 38
		private ToolStripMenuItem TSMenuItemCMDHighlightLastWords;

		// Token: 0x04000027 RID: 39
		private ToolStripMenuItem TSMenuItemWinStyleTopMost;

		// Token: 0x04000028 RID: 40
		private ToolStripSeparator toolStripSeparator12;

		// Token: 0x04000029 RID: 41
		private ToolStripMenuItem TSMenuItemOtherFunction;

		// Token: 0x0400002A RID: 42
		private ToolStripMenuItem TSMenuItemOtherFunctionCheckUpdate;

		// Token: 0x0400002B RID: 43
		private ToolStripMenuItem TSMenuItemOtherFunctionAbout;

		// Token: 0x0400002C RID: 44
		private ToolStripSeparator toolStripSeparator13;

		// Token: 0x0400002D RID: 45
		private ToolStripMenuItem TSMenuItemWinStyleNoShowInTaskBar;

		// Token: 0x0400002E RID: 46
		private ToolStripSeparator toolStripSeparator1;

		// Token: 0x0400002F RID: 47
		private RichTextBox RichTextBoxPython;

		// Token: 0x04000030 RID: 48
		private ToolStripMenuItem TSMenuItemWinStyleRightButtonDrag;

		// Token: 0x04000031 RID: 49
		private ToolStripSeparator toolStripSeparator2;

		// Token: 0x04000032 RID: 50
		private ToolStripMenuItem TSMenuItemWinStyleOpacity;

		// Token: 0x04000033 RID: 51
		private ToolStripMenuItem TSMenuItemWinStyleOpacity40;

		// Token: 0x04000034 RID: 52
		private ToolStripMenuItem TSMenuItemWinStyleOpacity50;

		// Token: 0x04000035 RID: 53
		private ToolStripMenuItem TSMenuItemWinStyleOpacity60;

		// Token: 0x04000036 RID: 54
		private ToolStripMenuItem TSMenuItemWinStyleOpacity70;

		// Token: 0x04000037 RID: 55
		private ToolStripMenuItem TSMenuItemWinStyleOpacity80;

		// Token: 0x04000038 RID: 56
		private ToolStripMenuItem TSMenuItemWinStyleOpacity90;

		// Token: 0x04000039 RID: 57
		private ToolStripMenuItem TSMenuItemWinStyleOpacity0;

		// Token: 0x0400003A RID: 58
		private ToolStripMenuItem TSMenuItemWinStyleOpacity10;

		// Token: 0x0400003B RID: 59
		private ToolStripMenuItem TSMenuItemWinStyleOpacity20;

		// Token: 0x0400003C RID: 60
		private ToolStripMenuItem TSMenuItemWinStyleOpacity30;

		// Token: 0x0400003D RID: 61
		private ToolStripMenuItem IconMenuItemResetWinform;

		// Token: 0x0400003E RID: 62
		private ToolStripSeparator toolStripSeparator3;

		// Token: 0x0400003F RID: 63
		private ToolStripMenuItem TSMenuItemOtherFunctionHelp;

		// Token: 0x04000040 RID: 64
		private ToolStripSeparator toolStripSeparator6;

		// Token: 0x04000041 RID: 65
		private ToolStripMenuItem TSMenuItemSaveAs;

		// Token: 0x04000042 RID: 66
		private ToolStripMenuItem 颜色ToolStripMenuItem;

		// Token: 0x04000043 RID: 67
		private ToolStripMenuItem TSMenuItemCMDBackColor;

		// Token: 0x04000044 RID: 68
		private ToolStripMenuItem TSMenuItemCMDBorderColor;

		// Token: 0x04000045 RID: 69
		private ToolStripMenuItem TSMenuItemCMDFontColor;

		// Token: 0x04000046 RID: 70
		private ToolStripSeparator toolStripSeparator4;

		// Token: 0x04000047 RID: 71
		private string fFileDir = "abaqus.rpy";

		// Token: 0x04000048 RID: 72
		private bool blAutoScroll = true;

		// Token: 0x04000049 RID: 73
		private DateTime fDateTimeLastWrite = default(DateTime);

		// Token: 0x0400004A RID: 74
		private bool blHighlightNewCmd = true;

		// Token: 0x0400004B RID: 75
		private int fLastRichTextBoxLength;

		// Token: 0x0400004C RID: 76
		private FileInfo filedir;

		// Token: 0x0400004D RID: 77
		private StreamReader reader;

		// Token: 0x0400004E RID: 78
		private FileStream fs;

		// Token: 0x0400004F RID: 79
		private string strCMD;

		// Token: 0x04000050 RID: 80
		private int fLastCMDLength;

		// Token: 0x04000051 RID: 81
		private int fLastReadLineNoOld;

		// Token: 0x04000052 RID: 82
		private int fLastReadLineNoNew;

		// Token: 0x04000053 RID: 83
		private Point frmLocationMouseOld = default(Point);

		// Token: 0x04000054 RID: 84
		private Point frmSizeOld = default(Point);

		// Token: 0x04000055 RID: 85
		private string strCurrentDirectory = Environment.CurrentDirectory;

		// Token: 0x04000056 RID: 86
		private int CurrentRichTextBoxPythonPos;

		// Token: 0x04000057 RID: 87
		private bool blNewOpenFile = true;

		// Token: 0x02000005 RID: 5
		private struct SCROLLINFO
		{
			// Token: 0x04000058 RID: 88
			public uint cbSize;

			// Token: 0x04000059 RID: 89
			public uint fMask;

			// Token: 0x0400005A RID: 90
			public int nMin;

			// Token: 0x0400005B RID: 91
			public int nMax;

			// Token: 0x0400005C RID: 92
			public uint nPage;

			// Token: 0x0400005D RID: 93
			public int nPos;

			// Token: 0x0400005E RID: 94
			public int nTrackPos;
		}

		// Token: 0x02000006 RID: 6
		private enum ScrollBarDirection
		{
			// Token: 0x04000060 RID: 96
			SB_HORZ,
			// Token: 0x04000061 RID: 97
			SB_VERT,
			// Token: 0x04000062 RID: 98
			SB_CTL,
			// Token: 0x04000063 RID: 99
			SB_BOTH
		}

		// Token: 0x02000007 RID: 7
		private enum ScrollInfoMask
		{
			// Token: 0x04000065 RID: 101
			SIF_RANGE = 1,
			// Token: 0x04000066 RID: 102
			SIF_PAGE,
			// Token: 0x04000067 RID: 103
			SIF_POS = 4,
			// Token: 0x04000068 RID: 104
			SIF_DISABLENOSCROLL = 8,
			// Token: 0x04000069 RID: 105
			SIF_TRACKPOS = 16,
			// Token: 0x0400006A RID: 106
			SIF_ALL = 23
		}
	}
}

