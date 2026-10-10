using System;
using System.CodeDom.Compiler;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;

namespace PythonReader.Properties
{
	// Token: 0x02000002 RID: 2
	[GeneratedCode("Microsoft.VisualStudio.Editors.SettingsDesigner.SettingsSingleFileGenerator", "9.0.0.0")]
	[CompilerGenerated]
	internal sealed partial class Settings : ApplicationSettingsBase
	{
		// Token: 0x17000001 RID: 1
		// (get) Token: 0x06000001 RID: 1 RVA: 0x00002050 File Offset: 0x00000250
		public static Settings Default
		{
			get
			{
				return Settings.defaultInstance;
			}
		}

		// Token: 0x17000002 RID: 2
		// (get) Token: 0x06000002 RID: 2 RVA: 0x00002057 File Offset: 0x00000257
		// (set) Token: 0x06000003 RID: 3 RVA: 0x00002069 File Offset: 0x00000269
		[UserScopedSetting]
		[DefaultSettingValue("True")]
		[DebuggerNonUserCode]
		public bool blTopmost
		{
			get
			{
				return (bool)this["blTopmost"];
			}
			set
			{
				this["blTopmost"] = value;
			}
		}

		// Token: 0x17000003 RID: 3
		// (get) Token: 0x06000004 RID: 4 RVA: 0x0000207C File Offset: 0x0000027C
		// (set) Token: 0x06000005 RID: 5 RVA: 0x0000208E File Offset: 0x0000028E
		[DefaultSettingValue("0")]
		[DebuggerNonUserCode]
		[UserScopedSetting]
		public int fWinfromLocationX
		{
			get
			{
				return (int)this["fWinfromLocationX"];
			}
			set
			{
				this["fWinfromLocationX"] = value;
			}
		}

		// Token: 0x17000004 RID: 4
		// (get) Token: 0x06000006 RID: 6 RVA: 0x000020A1 File Offset: 0x000002A1
		// (set) Token: 0x06000007 RID: 7 RVA: 0x000020B3 File Offset: 0x000002B3
		[UserScopedSetting]
		[DefaultSettingValue("0")]
		[DebuggerNonUserCode]
		public int fWinfromLocationY
		{
			get
			{
				return (int)this["fWinfromLocationY"];
			}
			set
			{
				this["fWinfromLocationY"] = value;
			}
		}

		// Token: 0x17000005 RID: 5
		// (get) Token: 0x06000008 RID: 8 RVA: 0x000020C6 File Offset: 0x000002C6
		// (set) Token: 0x06000009 RID: 9 RVA: 0x000020D8 File Offset: 0x000002D8
		[DefaultSettingValue("0")]
		[UserScopedSetting]
		[DebuggerNonUserCode]
		public int fWinformSizeX
		{
			get
			{
				return (int)this["fWinformSizeX"];
			}
			set
			{
				this["fWinformSizeX"] = value;
			}
		}

		// Token: 0x17000006 RID: 6
		// (get) Token: 0x0600000A RID: 10 RVA: 0x000020EB File Offset: 0x000002EB
		// (set) Token: 0x0600000B RID: 11 RVA: 0x000020FD File Offset: 0x000002FD
		[UserScopedSetting]
		[DefaultSettingValue("0")]
		[DebuggerNonUserCode]
		public int fWinformSizeY
		{
			get
			{
				return (int)this["fWinformSizeY"];
			}
			set
			{
				this["fWinformSizeY"] = value;
			}
		}

		// Token: 0x17000007 RID: 7
		// (get) Token: 0x0600000C RID: 12 RVA: 0x00002110 File Offset: 0x00000310
		// (set) Token: 0x0600000D RID: 13 RVA: 0x00002122 File Offset: 0x00000322
		[DefaultSettingValue("True")]
		[DebuggerNonUserCode]
		[UserScopedSetting]
		public bool blFirstRun
		{
			get
			{
				return (bool)this["blFirstRun"];
			}
			set
			{
				this["blFirstRun"] = value;
			}
		}

		// Token: 0x17000008 RID: 8
		// (get) Token: 0x0600000E RID: 14 RVA: 0x00002135 File Offset: 0x00000335
		// (set) Token: 0x0600000F RID: 15 RVA: 0x00002147 File Offset: 0x00000347
		[UserScopedSetting]
		[DebuggerNonUserCode]
		[DefaultSettingValue("1")]
		public int fFormBorderStyle
		{
			get
			{
				return (int)this["fFormBorderStyle"];
			}
			set
			{
				this["fFormBorderStyle"] = value;
			}
		}

		// Token: 0x17000009 RID: 9
		// (get) Token: 0x06000010 RID: 16 RVA: 0x0000215A File Offset: 0x0000035A
		// (set) Token: 0x06000011 RID: 17 RVA: 0x0000216C File Offset: 0x0000036C
		[DefaultSettingValue("True")]
		[DebuggerNonUserCode]
		[UserScopedSetting]
		public bool blWordwrap
		{
			get
			{
				return (bool)this["blWordwrap"];
			}
			set
			{
				this["blWordwrap"] = value;
			}
		}

		// Token: 0x1700000A RID: 10
		// (get) Token: 0x06000012 RID: 18 RVA: 0x0000217F File Offset: 0x0000037F
		// (set) Token: 0x06000013 RID: 19 RVA: 0x00002191 File Offset: 0x00000391
		[DefaultSettingValue("True")]
		[DebuggerNonUserCode]
		[UserScopedSetting]
		public bool blAutoScroll
		{
			get
			{
				return (bool)this["blAutoScroll"];
			}
			set
			{
				this["blAutoScroll"] = value;
			}
		}

		// Token: 0x1700000B RID: 11
		// (get) Token: 0x06000014 RID: 20 RVA: 0x000021A4 File Offset: 0x000003A4
		// (set) Token: 0x06000015 RID: 21 RVA: 0x000021B6 File Offset: 0x000003B6
		[UserScopedSetting]
		[DefaultSettingValue("True")]
		[DebuggerNonUserCode]
		public bool blHighlightNewCmd
		{
			get
			{
				return (bool)this["blHighlightNewCmd"];
			}
			set
			{
				this["blHighlightNewCmd"] = value;
			}
		}

		// Token: 0x1700000C RID: 12
		// (get) Token: 0x06000016 RID: 22 RVA: 0x000021C9 File Offset: 0x000003C9
		// (set) Token: 0x06000017 RID: 23 RVA: 0x000021DB File Offset: 0x000003DB
		[DefaultSettingValue("readme.txt")]
		[UserScopedSetting]
		[DebuggerNonUserCode]
		public string strLastFileName
		{
			get
			{
				return (string)this["strLastFileName"];
			}
			set
			{
				this["strLastFileName"] = value;
			}
		}

		// Token: 0x1700000D RID: 13
		// (get) Token: 0x06000018 RID: 24 RVA: 0x000021E9 File Offset: 0x000003E9
		// (set) Token: 0x06000019 RID: 25 RVA: 0x000021FB File Offset: 0x000003FB
		[DefaultSettingValue("Black")]
		[UserScopedSetting]
		[DebuggerNonUserCode]
		public Color FontColor
		{
			get
			{
				return (Color)this["FontColor"];
			}
			set
			{
				this["FontColor"] = value;
			}
		}

		// Token: 0x1700000E RID: 14
		// (get) Token: 0x0600001A RID: 26 RVA: 0x0000220E File Offset: 0x0000040E
		// (set) Token: 0x0600001B RID: 27 RVA: 0x00002220 File Offset: 0x00000420
		[DefaultSettingValue("宋体, 10.5pt")]
		[DebuggerNonUserCode]
		[UserScopedSetting]
		public Font Font
		{
			get
			{
				return (Font)this["Font"];
			}
			set
			{
				this["Font"] = value;
			}
		}

		// Token: 0x1700000F RID: 15
		// (get) Token: 0x0600001C RID: 28 RVA: 0x0000222E File Offset: 0x0000042E
		// (set) Token: 0x0600001D RID: 29 RVA: 0x00002240 File Offset: 0x00000440
		[UserScopedSetting]
		[DefaultSettingValue("True")]
		[DebuggerNonUserCode]
		public bool blNoShowInTaskBar
		{
			get
			{
				return (bool)this["blNoShowInTaskBar"];
			}
			set
			{
				this["blNoShowInTaskBar"] = value;
			}
		}

		// Token: 0x17000010 RID: 16
		// (get) Token: 0x0600001E RID: 30 RVA: 0x00002253 File Offset: 0x00000453
		// (set) Token: 0x0600001F RID: 31 RVA: 0x00002265 File Offset: 0x00000465
		[DebuggerNonUserCode]
		[DefaultSettingValue("True")]
		[UserScopedSetting]
		public bool blRightButtonDrag
		{
			get
			{
				return (bool)this["blRightButtonDrag"];
			}
			set
			{
				this["blRightButtonDrag"] = value;
			}
		}

		// Token: 0x17000011 RID: 17
		// (get) Token: 0x06000020 RID: 32 RVA: 0x00002278 File Offset: 0x00000478
		// (set) Token: 0x06000021 RID: 33 RVA: 0x0000228A File Offset: 0x0000048A
		[UserScopedSetting]
		[DebuggerNonUserCode]
		[DefaultSettingValue("1")]
		public double fOpacity
		{
			get
			{
				return (double)this["fOpacity"];
			}
			set
			{
				this["fOpacity"] = value;
			}
		}

		// Token: 0x17000012 RID: 18
		// (get) Token: 0x06000022 RID: 34 RVA: 0x0000229D File Offset: 0x0000049D
		// (set) Token: 0x06000023 RID: 35 RVA: 0x000022AF File Offset: 0x000004AF
		[DebuggerNonUserCode]
		[DefaultSettingValue("White")]
		[UserScopedSetting]
		public Color BackColor
		{
			get
			{
				return (Color)this["BackColor"];
			}
			set
			{
				this["BackColor"] = value;
			}
		}

		// Token: 0x17000013 RID: 19
		// (get) Token: 0x06000024 RID: 36 RVA: 0x000022C2 File Offset: 0x000004C2
		// (set) Token: 0x06000025 RID: 37 RVA: 0x000022D4 File Offset: 0x000004D4
		[DebuggerNonUserCode]
		[UserScopedSetting]
		[DefaultSettingValue("Gainsboro")]
		public Color BorderColor
		{
			get
			{
				return (Color)this["BorderColor"];
			}
			set
			{
				this["BorderColor"] = value;
			}
		}

		// Token: 0x04000001 RID: 1
		private static Settings defaultInstance = (Settings)SettingsBase.Synchronized(new Settings());
	}
}
