using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Security.Cryptography;
using System.IO;
using System.Linq;

namespace passgen
{
    /// <summary>
    /// Description of MainForm.
    /// </summary>
    public partial class MainForm : Form
    {
        List<string> colCapital = new List<string>(){"A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"};
        List<string> colLower   = new List<string>(){"a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "m", "n", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"};
        List<string> colDigits  = new List<string>(){"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"};
        List<string> colSymbols = new List<string>(){"!", "@", "#", "$", "%", "&", "*", "+", "=", "-", "."};        
          
        public string GetHash(string input)
        {
        //Расчёт хэша для расчёта сида генерации пароля
            var md5 = MD5.Create();
            var hash = md5.ComputeHash(System.Text.Encoding.UTF8.GetBytes(input));
            
            string result = "0x";
            foreach (var b in hash)
            {
                result += b.ToString("x2").ToUpper();
            }
            
            return result;
        }
        
        private void LoadServices()
        {
            if (File.Exists("services.txt"))
            {
                using (StreamReader sr = new StreamReader("services.txt"))
                {
                    string line;
                    while ((line = sr.ReadLine()) != null)
                    {
                        cmbService.Items.Add(line);
                    }
                }
            }
        }
        
        private void LoadSettings()
        {
            if (File.Exists("settings.txt"))
            {
                using (StreamReader sr = new StreamReader("settings.txt"))
                {
                    string line = sr.ReadLine();
                    if (line != null)
                    {
                        string[] settings = line.Split(',');
                        numLength.Value = Decimal.Parse(settings[0]);
                        cbCapital.Checked = settings[1] == "1" ? true : false;
                        cbLower.Checked = settings[2] == "1" ? true : false;
                        cbDigits.Checked = settings[3] == "1" ? true : false;
                        cbSymbols.Checked = settings[4] == "1" ? true : false;
                    }
                }
            }
        }
        
        private void SaveServices()
        {
            using (StreamWriter sw = new StreamWriter("services.txt", false))
            {
                for (int i = 0; i < cmbService.Items.Count; i++)
                {
                    sw.WriteLine(cmbService.Items[i].ToString());
                }
            }
        }

        private void SaveSettings()
        {
            using (StreamWriter sw = new StreamWriter("settings.txt", false))
            {
                string config = "";
                config += numLength.Value.ToString() + ",";
                config += cbCapital.Checked ? "1," : "0,";
                config += cbLower.Checked ? "1," : "0,";
                config += cbDigits.Checked ? "1," : "0,";
                config += cbSymbols.Checked ? "1" : "0";
                sw.WriteLine(config);
            }
        }
        
        public MainForm()
        {
            InitializeComponent();
        }
        void BtnGenerateClick(object sender, EventArgs e)
        {
            //Если сервис не вводился - добавить его в историю
            bool found = false;
            for (int i = 0; i < cmbService.Items.Count; i++){
                if (cmbService.Items[i].ToString() == cmbService.Text){
                    found = true;
                    break;
                }
            }
            
            if (!found && cmbService.Text != ""){
                cmbService.Items.Add(cmbService.Text);
            }
        
            //Определение используемых символов
            List<string> symbols = new List<string>(){};
            if (cbCapital.Checked == true){
                symbols.AddRange(colCapital);
            }
            if (cbLower.Checked == true){
                symbols.AddRange(colLower);
            }
            if (cbDigits.Checked == true){
                symbols.AddRange(colDigits);
            }
            if (cbSymbols.Checked == true){
                symbols.AddRange(colSymbols);
            }
            
            //Вычисление сида генерации
            int seed = 0;
            string seedString = cmbService.Text + tbSeed.Text + numLength.Value;
            if (seedString != ""){
                seed = Convert.ToInt32(GetHash(seedString).Substring(0, 10), 16);
            }
            else {
                seed = (int)(DateTime.Now.Subtract(new DateTime(1970, 1, 1))).TotalSeconds;
            }
            int SymbolsUsed = symbols.Count;
            int Length = Decimal.ToInt32(numLength.Value);
            string Password = "";
            
            //Генерация пароля
            Random rnd = new Random(seed);
            for (int i = 0; i < Length; i++)
            {
                Password = Password + symbols[rnd.Next(0, SymbolsUsed)];
            }
            
            //Выдача парооля
            tbPassword.Text = Password;
            this.ActiveControl = tbPassword;
        }
        void CmbServiceKeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter){
                BtnGenerateClick(null, null);
            }
        }
        void BtnCopyClick(object sender, EventArgs e)
        {
            Clipboard.SetText(tbPassword.Text);
        }
        void MainFormLoad(object sender, EventArgs e)
        {
            LoadServices();
            LoadSettings();
        }
        void MainFormFormClosing(object sender, FormClosingEventArgs e)
        {
            SaveServices();
            SaveSettings();
        }
        void TbPasswordKeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter){
                BtnCopyClick(null, null);
                this.ActiveControl = cmbService;
            }
        }
    }
}
