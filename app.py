#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import logging
import os
import fitz
import random
from functools import partial
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def _send(update, text):
    update.message.reply_text(text, reply_to_message_id=update.message.message_id, parse_mode='MarkdownV2')


def start(update: Update, context: CallbackContext) -> None:
    _send(update, 'Hi! Use /predict or /predict <page> <line> for a get predict.')


def get_prediction(update: Update, context: CallbackContext) -> None:
    with fitz.open(os.getenv('PDF_FILE')) as doc:
        page = None
        line = None

        try:
            page = int(context.args[0])
            line = int(context.args[1])
        except Exception:
            if len(context.args) > 0:
                _send(update, 'Usage: /predict or /predict <page> <line>')
            else:
                try:
                    ind = random.randrange(doc.page_count)
                    raw_page = _clear_page(ind + 1, doc[ind].getText())
                    text_ind = random.randrange(len(raw_page) - 1)
                    text = raw_page[text_ind].strip()
                    _send(update, f"Page: {ind + 1} \| Line: {text_ind + 1}\n```{text}```")
                except Exception as e:
                    logger.error(e)
                    _send(update, '🤡')
            return

        try:
            _send(update, f"```{_get(page, line, doc)}```")
        except IndexError as e:
            if str(e) == 'page not in document':
                _send(update, f"🚧 {page} page not found!")
            else:
                _send(update, f"🚧 {line} line not found!")
            return
        except Exception as e:
            logger.error(e)
            _send(update, '🤡')


def _get(page: int, row: int, doc: fitz.Document) -> str:
    return _clear_page(page, doc[page - 1].getText())[row - 1].strip()


def _clear_page(ind: int, text: str) -> str:
    return list(filter(lambda x: len(x) > 0 and x != str(ind), str(ind).join(text.split(str(ind))[1:]).split('\n')))


if __name__ == '__main__':
    load_dotenv()

    updater = Updater(os.getenv('BOT_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("predict", get_prediction))

    updater.start_polling()
    updater.idle()
