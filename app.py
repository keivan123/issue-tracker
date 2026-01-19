from flask import Flask, request, render_template, url_for, redirect
from db import init_db, get_db, init_users
from datetime import datetime

app = Flask(__name__)







@app.route("/")#this is the home page
def home():
    return render_template("home.html")



@app.route("/issues")#this is the issues.html page
def list_issues():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""SELECT id, title, status, priority, created_at FROM issues ORDER BY created_at
                DESC
 """)
    issues = cur.fetchall()

    conn.close()
    return render_template("issues.html",issues=issues)


@app.route("/issues/<int:issue_id>/edit", methods = ["GET","POST"])#this edits the issue
def edit_issue(issue_id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("""
            UPDATE issues
            SET title = ?, status = ?, priority = ?
            WHERE id = ?
        """, (
            request.form["title"],
            request.form["status"],
            request.form["priority"],
            issue_id
        ))

        conn.commit()
        conn.close()
        return redirect(url_for("list_issues"))

    cur.execute("""
        SELECT id, title, status, priority
        FROM issues
        WHERE id = ?
    """, (issue_id,))

    issue = cur.fetchone()
    conn.close()

    return render_template("edit_issue.html", issue=issue)




@app.route("/issues/<int:issue_id>/delete")#this delets a row from the table
def delete_issue(issue_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    conn.commit()
    conn.close()

    
    return redirect(url_for("list_issues"))


@app.route("/issues/<int:issue_id>/status/<new_status>")#this updates a row from the table
def update_status(issue_id,new_status):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE issues SET status = ? WHERE id = ?", (new_status,issue_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("list_issues"))




@app.route("/new", methods=["GET", "POST"])#this is the new_isues.html page
def new_issue():
    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO issues (title, status, priority, created_at) VALUES (?, ?, ?, ?)",
            (
                request.form["title"],
                request.form["status"],
                request.form["priority"],
                datetime.now().isoformat()
            )
        )

        conn.commit()
        conn.close()
        return "Issue created"

    return render_template("new_issue.html")

if __name__ == "__main__":
    init_db()
    init_users()
    app.run(debug=True)