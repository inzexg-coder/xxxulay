namespace passgen
{
    partial class MainForm
    {
        /// <summary>
        /// Designer variable used to keep track of non-visual components.
        /// </summary>
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox tbSeed;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.CheckBox cbCapital;
        private System.Windows.Forms.CheckBox cbLower;
        private System.Windows.Forms.CheckBox cbDigits;
        private System.Windows.Forms.CheckBox cbSymbols;
        private System.Windows.Forms.NumericUpDown numLength;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button btnGenerate;
        private System.Windows.Forms.TextBox tbPassword;
        private System.Windows.Forms.Button btnCopy;
        private System.Windows.Forms.ComboBox cmbService;
        
        /// <summary>
        /// Disposes resources used by the form.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing) {
                if (components != null) {
                    components.Dispose();
                }
            }
            base.Dispose(disposing);
        }
        
        /// <summary>
        /// This method is required for Windows Forms designer support.
        /// Do not change the method contents inside the source code editor. The Forms designer might
        /// not be able to load this method if it was changed manually.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.tbSeed = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.cbCapital = new System.Windows.Forms.CheckBox();
            this.cbLower = new System.Windows.Forms.CheckBox();
            this.cbDigits = new System.Windows.Forms.CheckBox();
            this.cbSymbols = new System.Windows.Forms.CheckBox();
            this.numLength = new System.Windows.Forms.NumericUpDown();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.btnGenerate = new System.Windows.Forms.Button();
            this.tbPassword = new System.Windows.Forms.TextBox();
            this.btnCopy = new System.Windows.Forms.Button();
            this.cmbService = new System.Windows.Forms.ComboBox();
            ((System.ComponentModel.ISupportInitialize)(this.numLength)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(0, 42);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(120, 16);
            this.label1.TabIndex = 0;
            this.label1.Text = "Название сервиса:";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // tbSeed
            // 
            this.tbSeed.Location = new System.Drawing.Point(136, 8);
            this.tbSeed.Name = "tbSeed";
            this.tbSeed.Size = new System.Drawing.Size(152, 20);
            this.tbSeed.TabIndex = 1;
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(0, 10);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(120, 16);
            this.label2.TabIndex = 2;
            this.label2.Text = "Сид-фраза:";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // cbCapital
            // 
            this.cbCapital.Checked = true;
            this.cbCapital.CheckState = System.Windows.Forms.CheckState.Checked;
            this.cbCapital.Location = new System.Drawing.Point(136, 104);
            this.cbCapital.Name = "cbCapital";
            this.cbCapital.Size = new System.Drawing.Size(128, 24);
            this.cbCapital.TabIndex = 5;
            this.cbCapital.Text = "Заглавные буквы";
            this.cbCapital.UseVisualStyleBackColor = true;
            // 
            // cbLower
            // 
            this.cbLower.Checked = true;
            this.cbLower.CheckState = System.Windows.Forms.CheckState.Checked;
            this.cbLower.Location = new System.Drawing.Point(136, 128);
            this.cbLower.Name = "cbLower";
            this.cbLower.Size = new System.Drawing.Size(128, 24);
            this.cbLower.TabIndex = 6;
            this.cbLower.Text = "Маленькие буквы";
            this.cbLower.UseVisualStyleBackColor = true;
            // 
            // cbDigits
            // 
            this.cbDigits.Checked = true;
            this.cbDigits.CheckState = System.Windows.Forms.CheckState.Checked;
            this.cbDigits.Location = new System.Drawing.Point(136, 152);
            this.cbDigits.Name = "cbDigits";
            this.cbDigits.Size = new System.Drawing.Size(128, 24);
            this.cbDigits.TabIndex = 7;
            this.cbDigits.Text = "Цифры";
            this.cbDigits.UseVisualStyleBackColor = true;
            // 
            // cbSymbols
            // 
            this.cbSymbols.Checked = true;
            this.cbSymbols.CheckState = System.Windows.Forms.CheckState.Checked;
            this.cbSymbols.Location = new System.Drawing.Point(136, 176);
            this.cbSymbols.Name = "cbSymbols";
            this.cbSymbols.Size = new System.Drawing.Size(128, 24);
            this.cbSymbols.TabIndex = 8;
            this.cbSymbols.Text = "Спецсимволы";
            this.cbSymbols.UseVisualStyleBackColor = true;
            // 
            // numLength
            // 
            this.numLength.Location = new System.Drawing.Point(136, 72);
            this.numLength.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.numLength.Name = "numLength";
            this.numLength.Size = new System.Drawing.Size(40, 20);
            this.numLength.TabIndex = 4;
            this.numLength.Value = new decimal(new int[] {
            10,
            0,
            0,
            0});
            // 
            // label3
            // 
            this.label3.Location = new System.Drawing.Point(0, 74);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(120, 16);
            this.label3.TabIndex = 9;
            this.label3.Text = "Длина:";
            this.label3.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // label4
            // 
            this.label4.Location = new System.Drawing.Point(0, 104);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(120, 16);
            this.label4.TabIndex = 10;
            this.label4.Text = "Символы:";
            this.label4.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // btnGenerate
            // 
            this.btnGenerate.Location = new System.Drawing.Point(8, 208);
            this.btnGenerate.Name = "btnGenerate";
            this.btnGenerate.Size = new System.Drawing.Size(280, 23);
            this.btnGenerate.TabIndex = 11;
            this.btnGenerate.Text = "Готово";
            this.btnGenerate.UseVisualStyleBackColor = true;
            this.btnGenerate.Click += new System.EventHandler(this.BtnGenerateClick);
            // 
            // tbPassword
            // 
            this.tbPassword.Location = new System.Drawing.Point(8, 240);
            this.tbPassword.Name = "tbPassword";
            this.tbPassword.Size = new System.Drawing.Size(280, 20);
            this.tbPassword.TabIndex = 12;
            this.tbPassword.KeyDown += new System.Windows.Forms.KeyEventHandler(this.TbPasswordKeyDown);
            // 
            // btnCopy
            // 
            this.btnCopy.Location = new System.Drawing.Point(8, 272);
            this.btnCopy.Name = "btnCopy";
            this.btnCopy.Size = new System.Drawing.Size(280, 23);
            this.btnCopy.TabIndex = 13;
            this.btnCopy.Text = "Скопировать";
            this.btnCopy.UseVisualStyleBackColor = true;
            this.btnCopy.Click += new System.EventHandler(this.BtnCopyClick);
            // 
            // cmbService
            // 
            this.cmbService.FormattingEnabled = true;
            this.cmbService.Location = new System.Drawing.Point(136, 40);
            this.cmbService.Name = "cmbService";
            this.cmbService.Size = new System.Drawing.Size(152, 21);
            this.cmbService.TabIndex = 2;
            this.cmbService.KeyDown += new System.Windows.Forms.KeyEventHandler(this.CmbServiceKeyDown);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(294, 299);
            this.Controls.Add(this.cmbService);
            this.Controls.Add(this.btnCopy);
            this.Controls.Add(this.tbPassword);
            this.Controls.Add(this.btnGenerate);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.numLength);
            this.Controls.Add(this.cbSymbols);
            this.Controls.Add(this.cbDigits);
            this.Controls.Add(this.cbLower);
            this.Controls.Add(this.cbCapital);
            this.Controls.Add(this.tbSeed);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "MainForm";
            this.Text = "passgen";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainFormFormClosing);
            this.Load += new System.EventHandler(this.MainFormLoad);
            ((System.ComponentModel.ISupportInitialize)(this.numLength)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }
    }
}
