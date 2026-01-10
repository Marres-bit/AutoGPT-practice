"""
Email notifier using SMTP. Requires SMTP credentials in `crypto_agent.config`.
"""
import smtplib
from email.message import EmailMessage
from typing import Optional
from pathlib import Path
from . import config


def send_email(subject: str, body: str, to: Optional[str] = None, attachment_path: Optional[Path] = None) -> bool:
    """Send an email using configured SMTP. Returns True on success."""
    to = to or config.EMAIL_RECIPIENT
    if not to:
        raise ValueError('No recipient provided and no EMAIL_RECIPIENT configured')

    if not config.SMTP_HOST or not config.SMTP_USER or not config.SMTP_PASS:
        raise RuntimeError('SMTP configuration missing (set SP_SMTP_HOST, SP_SMTP_USER, SP_SMTP_PASS)')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = config.SMTP_USER
    msg['To'] = to
    msg.set_content(body)

    # Attach file if provided
    if attachment_path and Path(attachment_path).exists():
        data = Path(attachment_path).read_bytes()
        maintype = 'application'
        subtype = 'octet-stream'
        try:
            # attempt simpler content type for .docx
            if str(attachment_path).lower().endswith('.docx'):
                maintype, subtype = 'application', 'vnd.openxmlformats-officedocument.wordprocessingml.document'
        except Exception:
            pass
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=Path(attachment_path).name)

    # Send via SMTP
    try:
        if config.SMTP_USE_TLS:
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=20) as server:
                server.starttls()
                server.login(config.SMTP_USER, config.SMTP_PASS)
                server.send_message(msg)
        else:
            with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, timeout=20) as server:
                server.login(config.SMTP_USER, config.SMTP_PASS)
                server.send_message(msg)
        return True
    except Exception as e:
        # bubble up or return False
        raise


def send_summary_email(summary_path: Path, report_path: Optional[Path] = None, recipient: Optional[str] = None) -> bool:
    """Send the textual summary file and attach the .docx if available."""
    if not Path(summary_path).exists():
        raise FileNotFoundError(f"Summary file not found: {summary_path}")
    body = Path(summary_path).read_text(encoding='utf-8')
    subject = 'SP Testnet - Cycle Summary'
    attachment = Path(report_path) if report_path and Path(report_path).exists() else None
    return send_email(subject, body, to=recipient or config.EMAIL_RECIPIENT, attachment_path=attachment)
