# 📊 Interactive Data Visualizer using Streamlit

This project is a **dynamic data visualization web app** built using Python’s Streamlit library. It allows users to upload `.xls` Excel files and interactively explore their data through **line charts, pie charts, and heat maps** — all rendered based on selected categories (columns) of the uploaded data.

---

## 🧠 What is Streamlit?

> **Streamlit** is an open-source Python library that makes it easy to build beautiful custom web apps for machine learning and data science projects — with no frontend experience required. All you need is Python!

Streamlit turns data scripts into shareable web apps in minutes, letting users interact with data through widgets like sliders, dropdowns, buttons, and file uploaders.

Official Site: [https://streamlit.io](https://streamlit.io)

---

## 🚀 Installation Guide (in PyCharm)

1. **Open PyCharm** and create or open your project.
2. Go to **Terminal** (bottom tab in PyCharm).
3. Activate your virtual environment (optional but recommended).
4. Run the following command to install Streamlit:

```bash
pip install streamlit
```

5. (Optional) Add the following to your `requirements.txt`:

```
streamlit
pandas
matplotlib
seaborn
openpyxl
```

---

## 📁 How to Run the Project

1. Save your Python Streamlit script, for example: `app.py`
2. Open terminal in the directory of the project and run:

```bash
streamlit run app.py
```

3. The app will launch in your default browser.

---

## 🔧 How It Works

### 📝 1. File Upload
- User uploads an `.xls` Excel file through the Streamlit file uploader widget.

### 🧩 2. Column Selection
- Once uploaded, Streamlit reads the data using **Pandas**.
- A sidebar or dropdown appears listing all the **column names** from the Excel file.
- User selects the columns they wish to analyze.

### 📊 3. Dynamic Visualization
- Based on the user's selection, the app automatically updates the following visualizations:

  - **📈 Line Chart:** Displays trends or progression of numerical data across the selected category.
  - **🥧 Pie Chart:** Shows distribution percentages for categorical values.
  - **🔥 Heat Map:** Represents the correlation between selected columns using color gradients.

All visualizations are interactive and update instantly when the user changes the selection.

---

## 📷 Example Screenshots

*(Add your screenshots here to showcase how the app looks)*

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **Matplotlib / Seaborn**
- **OpenPyXL** (for reading Excel files)

---

## 📌 To Do

- [ ] Add export/download option for filtered data
- [ ] Support `.xlsx` files
- [ ] Add user guide video or GIF

---

## 🙌 Contributing

Feel free to fork this repo, submit issues or pull requests. Feedback is always welcome!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

Created with ❤️ by **Aayush Bhandare**    
🌐 GitHub: [https://github.com/elephunt-fire]
