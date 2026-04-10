namespace Laba6
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            label1 = new Label();
            GameWhat = new TabPage();
            label3 = new Label();
            attemptsTextBox = new TextBox();
            textBoxResult = new TextBox();
            textBox1 = new TextBox();
            textBox2 = new TextBox();
            pictureBox1 = new PictureBox();
            label2 = new Label();
            result = new Label();
            checkGameWhat = new Button();
            labelB = new Label();
            labelA = new Label();
            Menu = new TabControl();
            arraySort = new TabPage();
            btnCompareSort = new Button();
            btnShellSort = new Button();
            btnBubbleSort = new Button();
            lblArraySize = new Label();
            lblArrayAverage = new Label();
            lblArrayMax = new Label();
            lblArrayMin = new Label();
            dataGridViewArray = new DataGridView();
            btnUpdateArrayStats = new Button();
            btnClearArray = new Button();
            btnGenerateRandom = new Button();
            btnCreateCustom = new Button();
            btnCreateDefault = new Button();
            txtArraySize = new TextBox();
            label4 = new Label();
            authorInfo = new TabPage();
            textAuthor = new Label();
            ConnectFourGameTab = new TabPage();
            resetGameBtn = new Button();
            StatusLabel = new Label();
            ScreenGame = new TableLayoutPanel();
            arrayProcessorBindingSource = new BindingSource(components);
            GameWhat.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).BeginInit();
            Menu.SuspendLayout();
            arraySort.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)dataGridViewArray).BeginInit();
            authorInfo.SuspendLayout();
            ConnectFourGameTab.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)arrayProcessorBindingSource).BeginInit();
            SuspendLayout();
            // 
            // label1
            // 
            resources.ApplyResources(label1, "label1");
            label1.Name = "label1";
            label1.Click += label1_Click;
            // 
            // GameWhat
            // 
            resources.ApplyResources(GameWhat, "GameWhat");
            GameWhat.Controls.Add(label3);
            GameWhat.Controls.Add(attemptsTextBox);
            GameWhat.Controls.Add(textBoxResult);
            GameWhat.Controls.Add(textBox1);
            GameWhat.Controls.Add(textBox2);
            GameWhat.Controls.Add(pictureBox1);
            GameWhat.Controls.Add(label2);
            GameWhat.Controls.Add(result);
            GameWhat.Controls.Add(checkGameWhat);
            GameWhat.Controls.Add(labelB);
            GameWhat.Controls.Add(labelA);
            GameWhat.Name = "GameWhat";
            GameWhat.UseVisualStyleBackColor = true;
            GameWhat.Click += GameWhat_Click;
            // 
            // label3
            // 
            resources.ApplyResources(label3, "label3");
            label3.Name = "label3";
            // 
            // attemptsTextBox
            // 
            resources.ApplyResources(attemptsTextBox, "attemptsTextBox");
            attemptsTextBox.Name = "attemptsTextBox";
            // 
            // textBoxResult
            // 
            resources.ApplyResources(textBoxResult, "textBoxResult");
            textBoxResult.Name = "textBoxResult";
            // 
            // textBox1
            // 
            resources.ApplyResources(textBox1, "textBox1");
            textBox1.Name = "textBox1";
            // 
            // textBox2
            // 
            resources.ApplyResources(textBox2, "textBox2");
            textBox2.Name = "textBox2";
            // 
            // pictureBox1
            // 
            resources.ApplyResources(pictureBox1, "pictureBox1");
            pictureBox1.Name = "pictureBox1";
            pictureBox1.TabStop = false;
            // 
            // label2
            // 
            resources.ApplyResources(label2, "label2");
            label2.Name = "label2";
            // 
            // result
            // 
            resources.ApplyResources(result, "result");
            result.Name = "result";
            // 
            // checkGameWhat
            // 
            resources.ApplyResources(checkGameWhat, "checkGameWhat");
            checkGameWhat.BackColor = Color.Honeydew;
            checkGameWhat.Cursor = Cursors.Hand;
            checkGameWhat.Name = "checkGameWhat";
            checkGameWhat.UseVisualStyleBackColor = false;
            checkGameWhat.Click += checkGameWhat_Click;
            // 
            // labelB
            // 
            resources.ApplyResources(labelB, "labelB");
            labelB.Name = "labelB";
            // 
            // labelA
            // 
            resources.ApplyResources(labelA, "labelA");
            labelA.Name = "labelA";
            // 
            // Menu
            // 
            resources.ApplyResources(Menu, "Menu");
            Menu.Controls.Add(GameWhat);
            Menu.Controls.Add(arraySort);
            Menu.Controls.Add(authorInfo);
            Menu.Controls.Add(ConnectFourGameTab);
            Menu.Name = "Menu";
            Menu.SelectedIndex = 0;
            Menu.SelectedIndexChanged += Menu_SelectedIndexChanged;
            // 
            // arraySort
            // 
            resources.ApplyResources(arraySort, "arraySort");
            arraySort.Controls.Add(btnCompareSort);
            arraySort.Controls.Add(btnShellSort);
            arraySort.Controls.Add(btnBubbleSort);
            arraySort.Controls.Add(lblArraySize);
            arraySort.Controls.Add(lblArrayAverage);
            arraySort.Controls.Add(lblArrayMax);
            arraySort.Controls.Add(lblArrayMin);
            arraySort.Controls.Add(dataGridViewArray);
            arraySort.Controls.Add(btnUpdateArrayStats);
            arraySort.Controls.Add(btnClearArray);
            arraySort.Controls.Add(btnGenerateRandom);
            arraySort.Controls.Add(btnCreateCustom);
            arraySort.Controls.Add(btnCreateDefault);
            arraySort.Controls.Add(txtArraySize);
            arraySort.Controls.Add(label4);
            arraySort.Name = "arraySort";
            arraySort.UseVisualStyleBackColor = true;
            arraySort.Click += arraySort_Click;
            // 
            // btnCompareSort
            // 
            resources.ApplyResources(btnCompareSort, "btnCompareSort");
            btnCompareSort.BackColor = Color.Lavender;
            btnCompareSort.Name = "btnCompareSort";
            btnCompareSort.UseVisualStyleBackColor = false;
            btnCompareSort.Click += btnCompareSort_Click_1;
            // 
            // btnShellSort
            // 
            resources.ApplyResources(btnShellSort, "btnShellSort");
            btnShellSort.BackColor = Color.Lavender;
            btnShellSort.Name = "btnShellSort";
            btnShellSort.UseVisualStyleBackColor = false;
            btnShellSort.Click += btnShellSort_Click_1;
            // 
            // btnBubbleSort
            // 
            resources.ApplyResources(btnBubbleSort, "btnBubbleSort");
            btnBubbleSort.BackColor = Color.Lavender;
            btnBubbleSort.Name = "btnBubbleSort";
            btnBubbleSort.UseVisualStyleBackColor = false;
            btnBubbleSort.Click += btnBubbleSort_Click_1;
            // 
            // lblArraySize
            // 
            resources.ApplyResources(lblArraySize, "lblArraySize");
            lblArraySize.Name = "lblArraySize";
            // 
            // lblArrayAverage
            // 
            resources.ApplyResources(lblArrayAverage, "lblArrayAverage");
            lblArrayAverage.Name = "lblArrayAverage";
            // 
            // lblArrayMax
            // 
            resources.ApplyResources(lblArrayMax, "lblArrayMax");
            lblArrayMax.Name = "lblArrayMax";
            lblArrayMax.Click += lblArrayMax_Click;
            // 
            // lblArrayMin
            // 
            resources.ApplyResources(lblArrayMin, "lblArrayMin");
            lblArrayMin.Name = "lblArrayMin";
            // 
            // dataGridViewArray
            // 
            resources.ApplyResources(dataGridViewArray, "dataGridViewArray");
            dataGridViewArray.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridViewArray.Name = "dataGridViewArray";
            // 
            // btnUpdateArrayStats
            // 
            resources.ApplyResources(btnUpdateArrayStats, "btnUpdateArrayStats");
            btnUpdateArrayStats.BackColor = Color.Lavender;
            btnUpdateArrayStats.Name = "btnUpdateArrayStats";
            btnUpdateArrayStats.UseVisualStyleBackColor = false;
            btnUpdateArrayStats.Click += btnUpdateArrayStats_Click_1;
            // 
            // btnClearArray
            // 
            resources.ApplyResources(btnClearArray, "btnClearArray");
            btnClearArray.BackColor = Color.MistyRose;
            btnClearArray.ForeColor = SystemColors.ActiveCaptionText;
            btnClearArray.Name = "btnClearArray";
            btnClearArray.UseVisualStyleBackColor = false;
            btnClearArray.Click += btnClearArray_Click_1;
            // 
            // btnGenerateRandom
            // 
            resources.ApplyResources(btnGenerateRandom, "btnGenerateRandom");
            btnGenerateRandom.BackColor = Color.Lavender;
            btnGenerateRandom.Name = "btnGenerateRandom";
            btnGenerateRandom.UseVisualStyleBackColor = false;
            btnGenerateRandom.Click += btnGenerateRandom_Click_1;
            // 
            // btnCreateCustom
            // 
            resources.ApplyResources(btnCreateCustom, "btnCreateCustom");
            btnCreateCustom.BackColor = Color.Honeydew;
            btnCreateCustom.Name = "btnCreateCustom";
            btnCreateCustom.UseVisualStyleBackColor = false;
            btnCreateCustom.Click += btnCreateCustom_Click_1;
            // 
            // btnCreateDefault
            // 
            resources.ApplyResources(btnCreateDefault, "btnCreateDefault");
            btnCreateDefault.BackColor = Color.Lavender;
            btnCreateDefault.Name = "btnCreateDefault";
            btnCreateDefault.UseVisualStyleBackColor = false;
            btnCreateDefault.Click += btnCreateDefault_Click;
            // 
            // txtArraySize
            // 
            resources.ApplyResources(txtArraySize, "txtArraySize");
            txtArraySize.Name = "txtArraySize";
            // 
            // label4
            // 
            resources.ApplyResources(label4, "label4");
            label4.Name = "label4";
            // 
            // authorInfo
            // 
            resources.ApplyResources(authorInfo, "authorInfo");
            authorInfo.BackColor = Color.White;
            authorInfo.Controls.Add(textAuthor);
            authorInfo.Name = "authorInfo";
            // 
            // textAuthor
            // 
            resources.ApplyResources(textAuthor, "textAuthor");
            textAuthor.Name = "textAuthor";
            // 
            // ConnectFourGameTab
            // 
            resources.ApplyResources(ConnectFourGameTab, "ConnectFourGameTab");
            ConnectFourGameTab.Controls.Add(resetGameBtn);
            ConnectFourGameTab.Controls.Add(StatusLabel);
            ConnectFourGameTab.Controls.Add(ScreenGame);
            ConnectFourGameTab.Name = "ConnectFourGameTab";
            ConnectFourGameTab.UseVisualStyleBackColor = true;
            // 
            // resetGameBtn
            // 
            resources.ApplyResources(resetGameBtn, "resetGameBtn");
            resetGameBtn.BackColor = Color.MistyRose;
            resetGameBtn.Name = "resetGameBtn";
            resetGameBtn.UseVisualStyleBackColor = false;
            resetGameBtn.Click += resetGameBtn_Click;
            // 
            // StatusLabel
            // 
            resources.ApplyResources(StatusLabel, "StatusLabel");
            StatusLabel.Name = "StatusLabel";
            // 
            // ScreenGame
            // 
            resources.ApplyResources(ScreenGame, "ScreenGame");
            ScreenGame.Name = "ScreenGame";
            // 
            // arrayProcessorBindingSource
            // 
            arrayProcessorBindingSource.DataSource = typeof(ArrayProcessor);
            // 
            // MainForm
            // 
            resources.ApplyResources(this, "$this");
            AutoScaleMode = AutoScaleMode.Font;
            Controls.Add(Menu);
            Controls.Add(label1);
            Name = "MainForm";
            FormClosing += MainForm_FormClosing;
            Load += MainForm_Load;
            GameWhat.ResumeLayout(false);
            GameWhat.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).EndInit();
            Menu.ResumeLayout(false);
            arraySort.ResumeLayout(false);
            arraySort.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)dataGridViewArray).EndInit();
            authorInfo.ResumeLayout(false);
            authorInfo.PerformLayout();
            ConnectFourGameTab.ResumeLayout(false);
            ConnectFourGameTab.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)arrayProcessorBindingSource).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label label1;
        private TabPage GameWhat;
        private Label label3;
        private TextBox attemptsTextBox;
        private TextBox textBoxResult;
        private TextBox textBox1;
        private TextBox textBox2;
        private PictureBox pictureBox1;
        private Label label2;
        private Label result;
        private Button checkGameWhat;
        private Label labelB;
        private Label labelA;
        private TabControl Menu;
        private TabPage arraySort;
        private TextBox txtArraySize;
        private Label label4;
        private Button button5;
        private Button button4;
        private Button button3;
        private Button button2;
        private Button btnCreateDefault;
        private DataGridView dataGridViewArray;
        private BindingSource arrayProcessorBindingSource;
        private Label lblArraySize;
        private Label lblArrayAverage;
        private Label lblArrayMax;
        private Label lblArrayMin;
        private Button button7;
        private Button button6;
        private Button btnBubbleSort;
        private TabPage authorInfo;
        private Label textAuthor;
        private TabPage ConnectFourGameTab;
        private TableLayoutPanel ScreenGame;
        private Label StatusLabel;
        private Button resetGameBtn;
    }
}