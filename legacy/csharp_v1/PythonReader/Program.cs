using System;
using System.Windows.Forms;

namespace PythonReader
{
	// Token: 0x02000003 RID: 3
	internal static class Program
	{
		// Token: 0x0600002A RID: 42 RVA: 0x00002309 File Offset: 0x00000509
		[STAThread]
		private static void Main()
		{
			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);
			Application.Run(new FormReader());
		}
	}
}
