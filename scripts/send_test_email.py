#!/usr/bin/env python3
"""
トラッキングピクセル入りのHTMLメールを SMTP 経由で送信する。

使い方 (Gmail):
  export SMTP_USER=you@gmail.com
  export SMTP_PASSWORD="xxxx xxxx xxxx xxxx"   # アプリパスワード

  python scripts/send_test_email.py \
    --to recipient@example.com \
    --tracking-url https://xxxxx.lambda-url.ap-northeast-1.on.aws/

使い方 (Xserver など任意の SMTP):
  python scripts/send_test_email.py \
    --to recipient@example.com \
    --tracking-url https://xxxxx.lambda-url.ap-northeast-1.on.aws/ \
    --smtp-host sv****.xserver.jp \
    --smtp-port 465
"""

import argparse
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GMAIL_HOST = "smtp.gmail.com"
DEFAULT_PORT = 465


def build_html(tracking_url: str, mail_id: str, user_id: str) -> str:
    pixel_url = f"{tracking_url.rstrip('/')}?mail_id={mail_id}&amp;user_id={user_id}"
    return f"""\
<html>
<body>
  <p>これはメール開封トラッキング PoC のテストメールです。</p>
  <img src="{pixel_url}" width="1" height="1" alt="">
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="トラッキングピクセル入りHTMLメールを送信する"
    )
    parser.add_argument("--to", required=True, help="送信先メールアドレス")
    parser.add_argument(
        "--tracking-url",
        required=True,
        help="Lambda Function URL (例: https://xxxxx.lambda-url.ap-northeast-1.on.aws/)",
    )
    parser.add_argument("--mail-id", default="test-001", help="メールID (default: test-001)")
    parser.add_argument("--user-id", default="user-001", help="ユーザーID (default: user-001)")
    parser.add_argument("--subject", default="[PoC] メール開封トラッキングテスト", help="件名")
    parser.add_argument("--verbose", action="store_true", help="送信する HTML を標準出力に表示する")
    parser.add_argument(
        "--smtp-host",
        default=os.environ.get("SMTP_HOST", GMAIL_HOST),
        help=f"SMTP サーバーホスト (環境変数 SMTP_HOST でも可, default: {GMAIL_HOST})",
    )
    parser.add_argument(
        "--smtp-port",
        type=int,
        default=int(os.environ.get("SMTP_PORT", DEFAULT_PORT)),
        help=f"SMTP ポート (環境変数 SMTP_PORT でも可, default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--smtp-user",
        default=os.environ.get("SMTP_USER"),
        help="送信元メールアドレス (環境変数 SMTP_USER でも可)",
    )
    parser.add_argument(
        "--smtp-password",
        default=os.environ.get("SMTP_PASSWORD"),
        help="SMTP パスワード (環境変数 SMTP_PASSWORD でも可)",
    )
    args = parser.parse_args()

    if not args.smtp_user or not args.smtp_password:
        parser.error(
            "SMTP_USER と SMTP_PASSWORD を環境変数またはオプション --smtp-user / --smtp-password で指定してください"
        )

    html_body = build_html(args.tracking_url, args.mail_id, args.user_id)

    if args.verbose:
        print("=== 送信する HTML ===")
        print(html_body)
        print("====================")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = args.subject
    msg["From"] = args.smtp_user
    msg["To"] = args.to
    msg.attach(MIMEText(html_body, "html"))

    print(f"接続中: {args.smtp_host}:{args.smtp_port} ...")
    with smtplib.SMTP_SSL(args.smtp_host, args.smtp_port) as smtp:
        smtp.login(args.smtp_user, args.smtp_password)
        smtp.sendmail(args.smtp_user, args.to, msg.as_string())

    pixel_url = f"{args.tracking_url.rstrip('/')}?mail_id={args.mail_id}&user_id={args.user_id}"
    print(f"送信完了 → {args.to}")
    print(f"トラッキングURL: {pixel_url}")


if __name__ == "__main__":
    main()
