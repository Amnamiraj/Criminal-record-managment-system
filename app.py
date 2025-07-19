from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pypyodbc as odbc
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'crms-secret-key-change-in-production'

# Database configuration for SQL Server using your connection details
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-JK48IIS'
DATABASE_NAME = 'CRMS'

def get_db_connection():
    """Create database connection using your configuration"""
    try:
        connection_string = f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trusted_Connection=yes;
        """
        conn = odbc.connect(connection_string)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Home page
@app.route('/')
def index():
    conn = get_db_connection()
    stats = {
        'criminals_count': 0,
        'active_cases': 0,
        'pending_firs': 0,
        'officers_count': 0
    }
    
    if conn:
        cursor = conn.cursor()
        try:
            # Count total criminals
            cursor.execute("SELECT COUNT(*) FROM Criminal")
            stats['criminals_count'] = cursor.fetchone()[0]
            
            # Count active cases (ongoing investigation reports)
            cursor.execute("SELECT COUNT(*) FROM Investigation_Report WHERE Case_Status = 'Ongoing'")
            stats['active_cases'] = cursor.fetchone()[0]
            
            # Count pending FIRs (Filed and In Progress status)
            cursor.execute("SELECT COUNT(*) FROM Complaint_FIR WHERE Status IN ('Filed', 'In Progress')")
            stats['pending_firs'] = cursor.fetchone()[0]
            
            # Count total officers
            cursor.execute("SELECT COUNT(*) FROM Police_Officer")
            stats['officers_count'] = cursor.fetchone()[0]
            
        except Exception as e:
            print(f"Error fetching statistics: {e}")
        finally:
            conn.close()
    
    return render_template('index.html', **stats)

# Criminal Management Routes
@app.route('/criminals')
def criminals():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Criminal")
        criminals = cursor.fetchall()
        conn.close()
        return render_template('criminals.html', criminals=criminals)
    return "Database connection failed", 500

@app.route('/criminals/add', methods=['GET', 'POST'])
def add_criminal():
    if request.method == 'POST':
        criminal_id = request.form['criminal_id']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        criminal_history = request.form['criminal_history']
        arrest_status = request.form['arrest_status']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Criminal (Criminal_ID, Name, Age, Gender, Address, Criminal_History, Arrest_Status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (criminal_id, name, age, gender, address, criminal_history, arrest_status))
            conn.commit()
            conn.close()
            flash('Criminal record added successfully!', 'success')
            return redirect(url_for('criminals'))
    
    return render_template('add_criminal.html')

@app.route('/criminals/edit/<int:criminal_id>', methods=['GET', 'POST'])
def edit_criminal(criminal_id):
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        criminal_history = request.form['criminal_history']
        arrest_status = request.form['arrest_status']
        
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Criminal 
            SET Name=?, Age=?, Gender=?, Address=?, Criminal_History=?, Arrest_Status=?
            WHERE Criminal_ID=?
        """, (name, age, gender, address, criminal_history, arrest_status, criminal_id))
        conn.commit()
        conn.close()
        flash('Criminal record updated successfully!', 'success')
        return redirect(url_for('criminals'))
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Criminal WHERE Criminal_ID=?", (criminal_id,))
    criminal = cursor.fetchone()
    conn.close()
    return render_template('edit_criminal.html', criminal=criminal)

# Crime Management Routes
@app.route('/crimes')
def crimes():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, cr.Name as Criminal_Name 
            FROM Crime c 
            LEFT JOIN Criminal cr ON c.Criminal_ID = cr.Criminal_ID
        """)
        crimes = cursor.fetchall()
        conn.close()
        return render_template('crimes.html', crimes=crimes)
    return "Database connection failed", 500

@app.route('/crimes/add', methods=['GET', 'POST'])
def add_crime():
    if request.method == 'POST':
        crime_id = request.form['crime_id']
        crime_type = request.form['crime_type']
        crime_date = request.form['crime_date']
        crime_location = request.form['crime_location']
        crime_description = request.form['crime_description']
        evidence_collected = request.form['evidence_collected']
        victim_id = request.form['victim_id'] if request.form['victim_id'] else None
        criminal_id = request.form['criminal_id'] if request.form['criminal_id'] else None
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Crime (Crime_ID, Crime_Type, Crime_Date, Crime_Location, 
                                 Crime_Description, Evidence_Collected, Victim_ID, Criminal_ID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (crime_id, crime_type, crime_date, crime_location, crime_description, 
                  evidence_collected, victim_id, criminal_id))
            conn.commit()
            conn.close()
            flash('Crime record added successfully!', 'success')
            return redirect(url_for('crimes'))
    
    # Get criminals for dropdown
    conn = get_db_connection()
    criminals = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Criminal_ID, Name FROM Criminal")
        criminals = cursor.fetchall()
        conn.close()
    
    return render_template('add_crime.html', criminals=criminals)

# FIR/Complaint Management Routes
@app.route('/firs')
def firs():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.*, p.Name as Officer_Name, c.Crime_Type
            FROM Complaint_FIR f
            LEFT JOIN Police_Officer p ON f.Filed_By = p.Officer_ID
            LEFT JOIN Crime c ON f.Crime_ID = c.Crime_ID
        """)
        firs = cursor.fetchall()
        conn.close()
        return render_template('firs.html', firs=firs)
    return "Database connection failed", 500

@app.route('/firs/add', methods=['GET', 'POST'])
def add_fir():
    if request.method == 'POST':
        complaint_id = request.form['complaint_id']
        complainant = request.form['complainant']
        crime_id = request.form['crime_id']
        complaint_date = request.form['complaint_date']
        description = request.form['description']
        filed_by = request.form['filed_by']
        status = request.form['status']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Complaint_FIR (Complaint_ID, Complainant, Crime_ID, Complaint_Date, 
                                         Description, Filed_By, Status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (complaint_id, complainant, crime_id, complaint_date, description, filed_by, status))
            conn.commit()
            conn.close()
            flash('FIR added successfully!', 'success')
            return redirect(url_for('firs'))
    
    # Get crimes and officers for dropdowns
    conn = get_db_connection()
    crimes = []
    officers = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Crime_ID, Crime_Type FROM Crime")
        crimes = cursor.fetchall()
        cursor.execute("SELECT Officer_ID, Name FROM Police_Officer")
        officers = cursor.fetchall()
        conn.close()
    
    return render_template('add_fir.html', crimes=crimes, officers=officers)

# Police Officers Management
@app.route('/officers')
def officers():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Police_Officer")
        officers = cursor.fetchall()
        conn.close()
        return render_template('officers.html', officers=officers)
    return "Database connection failed", 500

@app.route('/officers/add', methods=['GET', 'POST'])
def add_officer():
    if request.method == 'POST':
        officer_id = request.form['officer_id']
        name = request.form['name']
        rank = request.form['rank']
        badge_number = request.form['badge_number']
        contact_number = request.form['contact_number']
        police_station = request.form['police_station']
        assigned_cases = request.form['assigned_cases']
        crime_id = request.form['crime_id'] if request.form['crime_id'] else None
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Police_Officer (Officer_ID, Name, Rank, Badge_Number, Contact_Number, 
                                          PoliceStation, Assigned_Cases, Crime_ID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (officer_id, name, rank, badge_number, contact_number, police_station, assigned_cases, crime_id))
            conn.commit()
            conn.close()
            flash('Police officer added successfully!', 'success')
            return redirect(url_for('officers'))
    
    return render_template('add_officer.html')

# Victims Management
@app.route('/victims')
def victims():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.*, c.Crime_Type 
            FROM Victim v 
            LEFT JOIN Crime c ON v.Crime_ID = c.Crime_ID
        """)
        victims = cursor.fetchall()
        conn.close()
        return render_template('victims.html', victims=victims)
    return "Database connection failed", 500

@app.route('/victims/add', methods=['GET', 'POST'])
def add_victim():
    if request.method == 'POST':
        victim_id = request.form['victim_id']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        address = request.form['address']
        injury_status = request.form['injury_status']
        crime_id = request.form['crime_id']
        statement = request.form['statement']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Victim (Victim_ID, Name, Age, Gender, Contact_Number, Address, 
                                  Injury_Status, Crime_ID, Statement)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (victim_id, name, age, gender, contact_number, address, injury_status, crime_id, statement))
            conn.commit()
            conn.close()
            flash('Victim record added successfully!', 'success')
            return redirect(url_for('victims'))
    
    # Get crimes for dropdown
    conn = get_db_connection()
    crimes = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Crime_ID, Crime_Type FROM Crime")
        crimes = cursor.fetchall()
        conn.close()
    
    return render_template('add_victim.html', crimes=crimes)

# Suspects Management
@app.route('/suspects')
def suspects():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, c.Crime_Type 
            FROM Suspect s 
            LEFT JOIN Crime c ON s.Crime_ID = c.Crime_ID
        """)
        suspects = cursor.fetchall()
        conn.close()
        return render_template('suspects.html', suspects=suspects)
    return "Database connection failed", 500

@app.route('/suspects/add', methods=['GET', 'POST'])
def add_suspect():
    if request.method == 'POST':
        suspect_id = request.form['suspect_id']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        contact_number = request.form['contact_number']
        crime_id = request.form['crime_id']
        status = request.form['status']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Suspect (Suspect_ID, Name, Age, Gender, Address, Contact_Number, Crime_ID, Status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (suspect_id, name, age, gender, address, contact_number, crime_id, status))
            conn.commit()
            conn.close()
            flash('Suspect record added successfully!', 'success')
            return redirect(url_for('suspects'))
    
    # Get crimes for dropdown
    conn = get_db_connection()
    crimes = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Crime_ID, Crime_Type FROM Crime")
        crimes = cursor.fetchall()
        conn.close()
    
    return render_template('add_suspect.html', crimes=crimes)

# Evidence Management
@app.route('/evidence')
def evidence():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.*, c.Crime_Type 
            FROM Evidence e 
            LEFT JOIN Crime c ON e.Crime_ID = c.Crime_ID
        """)
        evidence_list = cursor.fetchall()
        conn.close()
        return render_template('evidence.html', evidence_list=evidence_list)
    return "Database connection failed", 500

@app.route('/evidence/add', methods=['GET', 'POST'])
def add_evidence():
    if request.method == 'POST':
        evidence_id = request.form['evidence_id']
        crime_id = request.form['crime_id']
        evidence_type = request.form['evidence_type']
        description = request.form['description']
        collected_by = request.form['collected_by']
        collection_date = request.form['collection_date']
        storage_location = request.form['storage_location']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Evidence (Evidence_ID, Crime_ID, Evidence_Type, Description, 
                                    Collected_By, Collection_Date, Storage_Location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (evidence_id, crime_id, evidence_type, description, collected_by, collection_date, storage_location))
            conn.commit()
            conn.close()
            flash('Evidence added successfully!', 'success')
            return redirect(url_for('evidence'))
    
    # Get crimes for dropdown
    conn = get_db_connection()
    crimes = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Crime_ID, Crime_Type FROM Crime")
        crimes = cursor.fetchall()
        conn.close()
    
    return render_template('add_evidence.html', crimes=crimes)

# Investigation Reports
@app.route('/reports')
def reports():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ir.*, c.Crime_Type, po.Name as Officer_Name
            FROM Investigation_Report ir
            LEFT JOIN Crime c ON ir.Crime_ID = c.Crime_ID
            LEFT JOIN Police_Officer po ON ir.Officer_ID = po.Officer_ID
        """)
        reports = cursor.fetchall()
        conn.close()
        return render_template('reports.html', reports=reports)
    return "Database connection failed", 500

@app.route('/reports/add', methods=['GET', 'POST'])
def add_report():
    if request.method == 'POST':
        report_id = request.form['report_id']
        crime_id = request.form['crime_id']
        officer_id = request.form['officer_id']
        investigation_details = request.form['investigation_details']
        findings = request.form['findings']
        report_date = request.form['report_date']
        case_status = request.form['case_status']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Investigation_Report (Report_ID, Crime_ID, Officer_ID, Investigation_Details, 
                                                Findings, Report_Date, Case_Status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (report_id, crime_id, officer_id, investigation_details, findings, report_date, case_status))
            conn.commit()
            conn.close()
            flash('Investigation report added successfully!', 'success')
            return redirect(url_for('reports'))
    
    # Get crimes and officers for dropdowns
    conn = get_db_connection()
    crimes = []
    officers = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Crime_ID, Crime_Type FROM Crime")
        crimes = cursor.fetchall()
        cursor.execute("SELECT Officer_ID, Name FROM Police_Officer")
        officers = cursor.fetchall()
        conn.close()
    
    return render_template('add_report.html', crimes=crimes, officers=officers)

# Court Cases Management
@app.route('/court-cases')
def court_cases():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cc.*, c.Crime_Type 
            FROM Court_Case cc 
            LEFT JOIN Crime c ON cc.Crime_ID = c.Crime_ID
        """)
        cases = cursor.fetchall()
        conn.close()
        return render_template('court_cases.html', cases=cases)
    return "Database connection failed", 500

@app.route('/court-cases/add', methods=['GET', 'POST'])
def add_court_case():
    if request.method == 'POST':
        case_id = request.form['case_id']
        crime_id = request.form['crime_id']
        court_name = request.form['court_name']
        judge_name = request.form['judge_name']
        hearing_date = request.form['hearing_date']
        case_status = request.form['case_status']
        verdict = request.form['verdict']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Court_Case (Case_ID, Crime_ID, Court_Name, Judge_Name, Hearing_Date, Case_Status, Verdict)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (case_id, crime_id, court_name, judge_name, hearing_date, case_status, verdict))
            conn.commit()
            conn.close()
            flash('Court case added successfully!', 'success')
            return redirect(url_for('court_cases'))
    
    # Get crimes for dropdown
    conn = get_db_connection()
    crimes = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Crime_ID, Crime_Type FROM Crime")
        crimes = cursor.fetchall()
        conn.close()
    
    return render_template('add_court_case.html', crimes=crimes)

# Witnesses Management
@app.route('/witnesses')
def witnesses():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT w.*, c.Crime_Type 
            FROM Witness w 
            LEFT JOIN Crime c ON w.Crime_ID = c.Crime_ID
        """)
        witnesses = cursor.fetchall()
        conn.close()
        return render_template('witnesses.html', witnesses=witnesses)
    return "Database connection failed", 500

@app.route('/witnesses/add', methods=['GET', 'POST'])
def add_witness():
    if request.method == 'POST':
        witness_id = request.form['witness_id']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        address = request.form['address']
        statement = request.form['statement']
        crime_id = request.form['crime_id']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Witness (Witness_ID, Name, Age, Gender, Contact_Number, Address, Statement, Crime_ID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (witness_id, name, age, gender, contact_number, address, statement, crime_id))
            conn.commit()
            conn.close()
            flash('Witness record added successfully!', 'success')
            return redirect(url_for('witnesses'))
    
    # Get crimes for dropdown
    conn = get_db_connection()
    crimes = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Crime_ID, Crime_Type FROM Crime")
        crimes = cursor.fetchall()
        conn.close()
    
    return render_template('add_witness.html', crimes=crimes)

# Search functionality
@app.route('/search')
def search():
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'criminal')
    
    if not query:
        return render_template('search.html', results=[], query='', search_type=search_type)
    
    conn = get_db_connection()
    results = []
    
    if conn:
        cursor = conn.cursor()
        
        if search_type == 'criminal':
            cursor.execute("SELECT * FROM Criminal WHERE Name LIKE ?", (f'%{query}%',))
        elif search_type == 'crime':
            cursor.execute("SELECT * FROM Crime WHERE Crime_Type LIKE ? OR Crime_Location LIKE ?", 
                         (f'%{query}%', f'%{query}%'))
        elif search_type == 'fir':
            cursor.execute("SELECT * FROM Complaint_FIR WHERE Complainant LIKE ? OR Description LIKE ?", 
                         (f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        conn.close()
    
    return render_template('search.html', results=results, query=query, search_type=search_type)

# Delete routes
@app.route('/delete/<table>/<int:record_id>')
def delete_record(table, record_id):
    table_configs = {
        'criminal': ('Criminal', 'Criminal_ID'),
        'crime': ('Crime', 'Crime_ID'),
        'fir': ('Complaint_FIR', 'Complaint_ID'),
        'officer': ('Police_Officer', 'Officer_ID'),
        'victim': ('Victim', 'Victim_ID'),
        'suspect': ('Suspect', 'Suspect_ID'),
        'evidence': ('Evidence', 'Evidence_ID'),
        'report': ('Investigation_Report', 'Report_ID'),
        'court_case': ('Court_Case', 'Case_ID'),
        'witness': ('Witness', 'Witness_ID')
    }
    
    if table not in table_configs:
        flash('Invalid table specified!', 'error')
        return redirect(url_for('index'))
    
    table_name, id_column = table_configs[table]
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = ?", (record_id,))
        conn.commit()
        conn.close()
        flash(f'{table_name} record deleted successfully!', 'success')
    
    return redirect(url_for(table + 's' if not table.endswith('s') else table))

if __name__ == '__main__':
    app.run(debug=True)