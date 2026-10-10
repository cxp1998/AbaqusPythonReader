using System;
using System.CodeDom.Compiler;
using System.ComponentModel;
using System.Diagnostics;
using System.Globalization;
using System.Resources;
using System.Runtime.CompilerServices;

namespace PythonReader.Properties
{
	// Token: 0x02000008 RID: 8
	[DebuggerNonUserCode]
	[GeneratedCode("System.Resources.Tools.StronglyTypedResourceBuilder", "2.0.0.0")]
	[CompilerGenerated]
	internal class Resources
	{
		// Token: 0x0600006D RID: 109 RVA: 0x00005011 File Offset: 0x00003211
		internal Resources()
		{
		}

		// Token: 0x17000014 RID: 20
		// (get) Token: 0x0600006E RID: 110 RVA: 0x0000501C File Offset: 0x0000321C
		[EditorBrowsable(EditorBrowsableState.Advanced)]
		internal static ResourceManager ResourceManager
		{
			get
			{
				if (object.ReferenceEquals(Resources.resourceMan, null))
				{
					ResourceManager resourceManager = new ResourceManager("PythonReader.Properties.Resources", typeof(Resources).Assembly);
					Resources.resourceMan = resourceManager;
				}
				return Resources.resourceMan;
			}
		}

		// Token: 0x17000015 RID: 21
		// (get) Token: 0x0600006F RID: 111 RVA: 0x0000505B File Offset: 0x0000325B
		// (set) Token: 0x06000070 RID: 112 RVA: 0x00005062 File Offset: 0x00003262
		[EditorBrowsable(EditorBrowsableState.Advanced)]
		internal static CultureInfo Culture
		{
			get
			{
				return Resources.resourceCulture;
			}
			set
			{
				Resources.resourceCulture = value;
			}
		}

		// Token: 0x17000016 RID: 22
		// (get) Token: 0x06000071 RID: 113 RVA: 0x0000506A File Offset: 0x0000326A
		internal static string UpdateData
		{
			get
			{
				return Resources.ResourceManager.GetString("UpdateData", Resources.resourceCulture);
			}
		}

		// Token: 0x17000017 RID: 23
		// (get) Token: 0x06000072 RID: 114 RVA: 0x00005080 File Offset: 0x00003280
		internal static string URLGoogleGroup
		{
			get
			{
				return Resources.ResourceManager.GetString("URLGoogleGroup", Resources.resourceCulture);
			}
		}

		// Token: 0x17000018 RID: 24
		// (get) Token: 0x06000073 RID: 115 RVA: 0x00005096 File Offset: 0x00003296
		internal static string URLUpdateCheck
		{
			get
			{
				return Resources.ResourceManager.GetString("URLUpdateCheck", Resources.resourceCulture);
			}
		}

		// Token: 0x17000019 RID: 25
		// (get) Token: 0x06000074 RID: 116 RVA: 0x000050AC File Offset: 0x000032AC
		internal static string Version
		{
			get
			{
				return Resources.ResourceManager.GetString("Version", Resources.resourceCulture);
			}
		}

		// Token: 0x0400006B RID: 107
		private static ResourceManager resourceMan;

		// Token: 0x0400006C RID: 108
		private static CultureInfo resourceCulture;
	}
}

