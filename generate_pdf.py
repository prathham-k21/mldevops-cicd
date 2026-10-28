import os
from fpdf import FPDF

class ReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', '', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'CICD pipeline and Monitoring Tools', 0, 1, 'C')
        self.ln(2)

    def footer(self):
        pass

def generate_pdf():
    pdf = ReportPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(18, 14, 18)
    pdf.set_auto_page_break(auto=True, margin=15)

    # ==================== PAGE 1 ====================
    pdf.add_page()
    pdf.ln(30)

    # Title
    pdf.set_font('Arial', 'B', 22)
    pdf.set_text_color(23, 71, 110) # #17476E
    pdf.cell(0, 12, 'CICD pipeline and Monitoring Tools', 0, 1, 'C')
    pdf.cell(0, 12, 'Summary Report', 0, 1, 'C')
    pdf.ln(25)

    # Table
    col_w1 = 52
    col_w2 = 122
    row_h = 11

    # Header Row
    pdf.set_fill_color(23, 71, 110)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_draw_color(180, 195, 210)
    pdf.cell(col_w1, row_h, 'Details', 1, 0, 'L', fill=True)
    pdf.cell(col_w2, row_h, 'Student Entry', 1, 1, 'L', fill=True)

    table_data = [
        ("Student Name", "Pratham Kadam"),
        ("Roll Number(s)", "DS 14 (PRN: 2324000362)"),
        ("Department / Class", "Final Year B.Tech CSE (Data Science) - Semester VII"),
        ("Academic Year", "A.Y 2026-27"),
        ("GitHub Repository URL", "https://github.com/prathham-k21/mldevops-cicd.git")
    ]

    for label, val in table_data:
        pdf.set_draw_color(180, 195, 210)
        pdf.set_fill_color(248, 250, 252)
        pdf.set_text_color(30, 41, 59)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_w1, row_h, f" {label}", 1, 0, 'L', fill=True)

        pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(0, 45, 98) # Dark blue
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_w2, row_h, f" {val}", 1, 1, 'L', fill=True)

    # ==================== PAGE 2 ====================
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)

    # Section 1: Problem Statement
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 7, '1. Problem Statement', 0, 1, 'L')
    pdf.set_font('Arial', '', 9.5)
    pdf.set_text_color(35, 35, 35)
    ps_text = (
        "Develop an end-to-end Machine Learning Web Application for Heart Disease Risk Prediction (CardioPulse) "
        "and implement the DevOps lifecycle on a Windows PC. The project utilizes Scikit-Learn for training a robust "
        "clinical risk classification model and Flask for delivering both a responsive web interface and REST API endpoints. "
        "Use Git for version control, GitHub for source-code hosting, Docker for application containerization, and "
        "Jenkins for automating the build, testing, and deployment process (including automated pytest suites). In addition, "
        "Prometheus monitoring and telemetry endpoints are integrated to observe real-time latency, request rates, "
        "and prediction distribution. Configure each tool, verify its installed version, and execute the necessary Windows "
        "commands to understand how the application moves from development to deployment."
    )
    pdf.multi_cell(0, 4.8, ps_text)
    pdf.ln(3)

    # Section 2: Tools: Environment Setup
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 7, '2. Tools: Environment Setup', 0, 1, 'L')
    pdf.ln(1)

    # Tool 1
    pdf.set_font('Arial', 'B', 10.5)
    pdf.cell(0, 6, '1. Python and Flask -- Web Application Development', 0, 1, 'L')

    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '1. Environment Setup', 0, 1, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Install Python and configure the system PATH.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Install Flask, Scikit-Learn, Pandas, Joblib, Prometheus Client, and Pytest.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Train and verify the Heart Disease model via train.py, generating model artifact.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Verify the installed versions of Python and pip, and run unit tests.', 0, 1, 'L')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '2. Commands to Run on Windows', 0, 1, 'L')
    pdf.set_font('Courier', '', 9)
    pdf.set_text_color(20, 20, 20)
    cmds_t1 = [
        "python --version",
        "pip --version",
        "pip install -r requirements.txt",
        "python train.py",
        "python -m pytest -v",
        "python app.py"
    ]
    for c in cmds_t1:
        pdf.cell(5)
        pdf.cell(0, 4.5, chr(149) + " " + c, 0, 1, 'L')
    pdf.ln(2)

    # Tool 2: Git
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 10.5)
    pdf.cell(0, 6, '2. Git -- Version Control', 0, 1, 'L')

    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '1. Environment Setup', 0, 1, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Install Git for Windows.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Configure the Git username and email, and verify the installed Git version.', 0, 1, 'L')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '2. Commands to Run on Windows', 0, 1, 'L')
    pdf.set_font('Courier', '', 9)
    pdf.set_text_color(20, 20, 20)
    cmds_t2 = [
        "git --version",
        "git init",
        "git status",
        "git add .",
        "git commit -m \"feat: complete MLOps CI/CD & Monitoring project with report\""
    ]
    for c in cmds_t2:
        pdf.cell(5)
        pdf.cell(0, 4.5, chr(149) + " " + c, 0, 1, 'L')
    pdf.ln(2)

    # Tool 3: GitHub
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 10.5)
    pdf.cell(0, 6, '3. GitHub -- Source-Code Hosting', 0, 1, 'L')

    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '1. Environment Setup', 0, 1, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Create a GitHub account and a remote repository.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Configure Git authentication using an appropriate method, such as Git Credential Manager or SSH.', 0, 1, 'L')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '2. Commands to Run on Windows', 0, 1, 'L')
    pdf.set_font('Arial', 'I', 8.5)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(5)
    pdf.cell(0, 4.5, 'Configured with the actual URL of the GitHub repository:', 0, 1, 'L')
    pdf.set_font('Courier', '', 9)
    pdf.set_text_color(20, 20, 20)
    cmds_t3 = [
        "git remote add origin https://github.com/prathham-k21/mldevops-cicd.git",
        "git branch -M main",
        "git push -u origin main",
        "git pull origin main"
    ]
    for c in cmds_t3:
        pdf.cell(5)
        pdf.cell(0, 4.5, chr(149) + " " + c, 0, 1, 'L')

    # ==================== PAGE 3 ====================
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)

    # Tool 4: Docker
    pdf.set_font('Arial', 'B', 10.5)
    pdf.cell(0, 6, '4. Docker -- Application Containerization', 0, 1, 'L')

    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '1. Environment Setup', 0, 1, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Install Docker Desktop and configure WSL 2 if required.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Verify the Docker Engine status and installed Docker and Docker Compose versions.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Construct Dockerfile specifying base image, dependencies, exposed ports, and healthcheck probe.', 0, 1, 'L')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '2. Commands to Run on Windows', 0, 1, 'L')
    pdf.set_font('Courier', '', 9)
    pdf.set_text_color(20, 20, 20)
    cmds_t4 = [
        "docker --version",
        "docker compose version",
        "docker info",
        "docker build -t cardiopulse-ml-app .",
        "docker run -d -p 5000:5000 --name cardiopulse-service cardiopulse-ml-app",
        "docker ps"
    ]
    for c in cmds_t4:
        pdf.cell(5)
        pdf.cell(0, 4.5, chr(149) + " " + c, 0, 1, 'L')
    pdf.ln(3)

    # Tool 5: Jenkins
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 10.5)
    pdf.cell(0, 6, '5. Jenkins -- Continuous Integration and Continuous Deployment', 0, 1, 'L')

    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '1. Environment Setup', 0, 1, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Install a Java JDK version compatible with the selected Jenkins release.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Install and configure Jenkins, and verify the Java and Jenkins versions.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Configure the required Git and Docker integrations for the pipeline using Jenkinsfile.', 0, 1, 'L')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '2. Commands to Run on Windows', 0, 1, 'L')

    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(3)
    pdf.cell(0, 4.5, 'For Jenkins installed directly on Windows:', 0, 1, 'L')
    pdf.set_font('Courier', '', 9)
    pdf.set_text_color(20, 20, 20)
    cmds_j_win = [
        "java -version",
        "git --version",
        "docker --version",
        "jenkins.exe start -- only if using a Jenkins installation that provides this service command."
    ]
    for c in cmds_j_win:
        pdf.cell(6)
        pdf.cell(0, 4.5, chr(149) + " " + c, 0, 1, 'L')

    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(3)
    pdf.cell(0, 4.5, 'For Jenkins running as a Docker container named jenkins:', 0, 1, 'L')
    pdf.set_font('Courier', '', 9)
    pdf.set_text_color(20, 20, 20)
    cmds_j_doc = [
        "docker run -d -p 8080:8080 -p 50000:50000 --name jenkins jenkins/jenkins:lts",
        "docker ps",
        "docker logs jenkins",
        "docker start jenkins",
        "docker exec jenkins java -version"
    ]
    for c in cmds_j_doc:
        pdf.cell(6)
        pdf.cell(0, 4.5, chr(149) + " " + c, 0, 1, 'L')
    pdf.ln(3)

    # Tool 6: Monitoring Tools
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 10.5)
    pdf.cell(0, 6, '6. Monitoring Tools -- Prometheus & Health Telemetry', 0, 1, 'L')

    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '1. Environment Setup', 0, 1, 'L')
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Integrate prometheus-client into Flask application to collect real-time HTTP metrics.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Configure health probe endpoint (/health) for container liveness and readiness verification.', 0, 1, 'L')
    pdf.cell(5)
    pdf.cell(0, 4.5, chr(149) + ' Expose Prometheus telemetry endpoint (/metrics) to track latency and prediction drift.', 0, 1, 'L')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 9.5)
    pdf.cell(0, 5, '2. Commands to Run on Windows', 0, 1, 'L')
    pdf.set_font('Courier', '', 9)
    pdf.set_text_color(20, 20, 20)
    cmds_t6 = [
        "curl -s http://localhost:5000/health",
        "curl -s http://localhost:5000/metrics",
        "curl -X POST http://localhost:5000/predict -H \"Content-Type: application/json\" -d \"{\\\"age\\\":55,...}\""
    ]
    for c in cmds_t6:
        pdf.cell(5)
        pdf.cell(0, 4.5, chr(149) + " " + c, 0, 1, 'L')

    output_path = "LAB-ISE2-CICD_pipeline_and_Monitoring_Tools.pdf"
    pdf.output(output_path, 'F')
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    generate_pdf()
