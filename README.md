# Book Oracle Bot

Small bot for predicting the day by page and line (or random) from PDF book.

## Commands

    - `/help` / `/start` - Use guide
    - `/predict` - Get random predict from book.
    - `/predict <page> <line>` - Get selected page and line predict from book.

## Deploy

1. Get Python 3.7+

2. Create `.env`:

    ```
    BOT_TOKEN=<telegram_bot_token>
    PDF_FILE=<path_to_pdf_book>
    ```

3. Run `app.py`
