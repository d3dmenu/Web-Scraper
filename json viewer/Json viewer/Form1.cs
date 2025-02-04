﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
using BjSTools.File;
using System.Net;

namespace Json_viewer
{
    public partial class Form1 : Form
    {

        string nodeText;

        public Form1()
        {
            InitializeComponent();  
        }

        #region UI events

        #endregion
        #region Helpers

        private TreeNode ConvertToTreeNode(BjSJsonObject obj, string name)
        {
            //TreeNode root = new TreeNode(String.Format(String.IsNullOrEmpty(name) ? "Object{{{1}}}" : "\"{0}\" : Object{{{1}}}", name, obj.Count));
            TreeNode root = new TreeNode(String.Format(String.IsNullOrEmpty(name) ? "Object{{{0}}}" : "\"{0}\"", name));
            root.ImageIndex = 0;
            root.SelectedImageIndex = 0;

            foreach (BjSJsonObjectMember member in obj)
            {
                switch (member.ValueKind)
                {
                    case BjSJsonValueKind.Object:
                        root.Nodes.Add(ConvertToTreeNode(member.Value as BjSJsonObject, member.Name));
                        break;
                    case BjSJsonValueKind.Array:
                        root.Nodes.Add(ConvertToTreeNode(member.Value as BjSJsonArray, member.Name));
                        break;
                    case BjSJsonValueKind.String:
                        root.Nodes.Add(new TreeNode(String.Format("\"{0}\" : \"{1}\"", member.Name, member.Value)) { ImageIndex = 2, SelectedImageIndex = 2 });
                        break;
                    case BjSJsonValueKind.Number:
                        root.Nodes.Add(new TreeNode(String.Format("\"{0}\" : {1}", member.Name, member.Value)) { ImageIndex = 3, SelectedImageIndex = 3 });
                        break;
                    case BjSJsonValueKind.Boolean:
                        root.Nodes.Add(new TreeNode(String.Format("\"{0}\" : {1}", member.Name, member.Value)) { ImageIndex = 4, SelectedImageIndex = 4 });
                        break;
                    case BjSJsonValueKind.Null:
                        root.Nodes.Add(new TreeNode(String.Format("\"{0}\" : null", member.Name)) { ImageIndex = 5, SelectedImageIndex = 5 });
                        break;
                    default:
                        break;
                }
            }

            return root;
        }
        private TreeNode ConvertToTreeNode(BjSJsonArray arr, string name)
        {
            TreeNode root = new TreeNode(String.Format(String.IsNullOrEmpty(name) ? "Array[{1}]" : "\"{0}\" : Array[{1}]", name, arr.Count));
            root.ImageIndex = 1;
            root.SelectedImageIndex = 1;

            for (int i = 0; i < arr.Count; i++)
            {
                var obj = arr[i];
                switch (BjSJsonHelper.GetValueKind(obj))
                {
                    case BjSJsonValueKind.Object:
                        root.Nodes.Add(ConvertToTreeNode(obj as BjSJsonObject, i.ToString()));
                        break;
                    case BjSJsonValueKind.Array:
                        root.Nodes.Add(ConvertToTreeNode(obj as BjSJsonArray, i.ToString()));
                        break;
                    case BjSJsonValueKind.String:
                        root.Nodes.Add(new TreeNode(String.Format("{0} : \"{1}\"", i, obj)) { ImageIndex = 2, SelectedImageIndex = 2 });
                        break;
                    case BjSJsonValueKind.Number:
                        root.Nodes.Add(new TreeNode(String.Format("{0} : {1}", i, obj)) { ImageIndex = 3, SelectedImageIndex = 3 });
                        break;
                    case BjSJsonValueKind.Boolean:
                        root.Nodes.Add(new TreeNode(String.Format("{0} : {1}", i, obj)) { ImageIndex = 4, SelectedImageIndex = 4 });
                        break;
                    case BjSJsonValueKind.Null:
                        root.Nodes.Add(new TreeNode(String.Format("{0} : null", i)) { ImageIndex = 5, SelectedImageIndex = 5 });
                        break;
                    default:
                        break;
                }
            }

            return root;
        }

        public static string WGet(string url)
        {
            string result = String.Empty;

            HttpWebRequest req = (HttpWebRequest)HttpWebRequest.Create(url);
            req.UserAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0";
            req.Timeout = 10000;
            req.Method = "GET";

            HttpWebResponse res = (HttpWebResponse)req.GetResponse();
            if (res.StatusCode == HttpStatusCode.OK)
            {
                StreamReader s = new StreamReader(res.GetResponseStream());
                result = s.ReadToEnd();
            }
            else
                throw new Exception(String.Format("{0}: {1}", res.StatusCode, res.StatusDescription));

            res.Close();

            return result;
        }

        #endregion
        private void LoadData(string data)
        {
            BjSJsonObject json = new BjSJsonObject(data);

            lstJsonTree.Nodes.Clear();

            TreeNode root = ConvertToTreeNode(json, String.Empty);
            foreach (TreeNode node in root.Nodes)
            {
                lstJsonTree.Nodes.Add(node);
                node.Expand();
            }

            txtImportText.Text = json.ToJsonString(false);

            tabControl1.SelectedIndex = 1;
        }

        private void btnfetchurl_Click(object sender, EventArgs e)
        {
            try
            {
                string content = WGet(txtimporturl.Text);
                if (String.IsNullOrEmpty(content))
                    throw new Exception("No data received!");

                LoadData(content);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void btnimportfileselect_Click_1(object sender, EventArgs e)
        {
            OpenFileDialog d = new OpenFileDialog();
            d.Multiselect = false;
            if (d.ShowDialog() == DialogResult.OK)  
            {
                txtimportfile.Text = d.FileName;
            }

            string data = String.Empty;
            try
            {
                using (StreamReader s = new StreamReader(txtimportfile.Text))
                {
                    data = s.ReadToEnd();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                return;
            }
            LoadData(data);
            Imager();
        }

        private void Imager() {
            if (lstJsonTree.Nodes.Count == 0)
            {
                pictureBox1.Visible = true;
            }
            else
            {
                pictureBox1.Visible = false;
            }
        }

        private void btnImportTextPaste_Click_1(object sender, EventArgs e)
        {
            try
            {
                if (Clipboard.ContainsText())
                    txtImportText.Text = Clipboard.GetText();
            }
            catch { }
        }

        private void btnImportTextLoad_Click(object sender, EventArgs e)
        {
            if (String.IsNullOrEmpty(txtImportText.Text))
            {
                MessageBox.Show("Empty path name is not legal.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else {
                try
                {
                    if (Clipboard.ContainsText())
                        txtImportText.Text = Clipboard.GetText();
                        LoadData(txtImportText.Text);
                }
                catch { }
            }
            Imager();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string data = String.Empty;
            try
            {
                using (StreamReader s = new StreamReader(txtimportfile.Text))
                {
                    data = s.ReadToEnd();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            LoadData(data);
        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            string data = String.Empty;
            try
            {
                using (StreamReader s = new StreamReader(txtimportfile.Text))
                {
                    data = s.ReadToEnd();
                }
                LoadData(data);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return; 
            }
            Imager();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (String.IsNullOrEmpty(txtImportText.Text))
            {
                MessageBox.Show("Cannot format string to json text", "Error", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
            }
            else
            {
                try
                {
                    if (Clipboard.ContainsText())
                        txtImportText.Text = Clipboard.GetText();
                }
                catch { }
            }
            Imager();
        }

        private void lstJsonTree_MouseDown(object sender, MouseEventArgs e)
        {
            try
            {
                if (e.Button == MouseButtons.Right)
                {
                    Point p = new Point(e.X, e.Y);

                    TreeNode node = lstJsonTree.GetNodeAt(p);

                    nodeText = node.Text;
                }
            }
            catch { }
        }

        private void copyToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                //Clipboard.SetText(nodeText, TextDataFormat.Text);
                Clipboard.SetText(nodeText.Replace("\"", ""), TextDataFormat.Text);
            }
            catch { }
        }
        private void Form1_Load(object sender, EventArgs e)
        {

        }


        private void FindRecursive(TreeNode treeNode, string searchString, Boolean foundFirst)  
        {  
            Boolean found = foundFirst;  
            foreach (TreeNode tn in treeNode.Nodes)  
            {

                if (tn.Text.ToUpper().Contains(searchString) && (!found))
                {
                    found = true;
                    lstJsonTree.SelectedNode = tn;
                    lstJsonTree.Focus();
                    tn.BackColor = Color.Yellow;
                    tn.Expand();
                }
                else
                {
                    tn.BackColor = Color.White;
                }
                FindRecursive(tn, searchString.ToUpper(), found);  
            }  
        } 

        private void searching()
        {
            try
            {
                if (txtsearch.Text.Trim() != "")
                {
                    string SearchStr = txtsearch.Text.ToUpper();
                    FindRecursive(lstJsonTree.Nodes[0], SearchStr, false);
                }
                //lstJsonTree.SelectedNode.Expand();
            }
            catch { }
        }

        private void btnSearch_Click(object sender, EventArgs e)
        {
            searching();
        }

        private void txtsearch_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                searching();
            }
        }

        private void lstJsonTree_NodeMouseClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            if (e.Button == MouseButtons.Right)
            {
                lstJsonTree.SelectedNode = e.Node;
            }
        }
    }
}
