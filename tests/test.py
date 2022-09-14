import logging
from datetime import datetime as dt

logging.basicConfig(filename='../logs/avito_logger.log',
                    filemode='a',
                    format='%(today)s | %(levelname)s: %(message)s',
                    level=logging.INFO)


def test_func(msg: str):
    current_date = dt.now().strftime("%Y-%m-%d, %H:%M:%S")
    logging.info({'today': current_date,
                                                            'levelname': 'INFO',
                                                            'message': 'Start test_func'})
    try:
        print(msg / 0)
        logging.info({'today': current_date,
                                                                'levelname': 'INFO',
                                                                'message': 'Message printed'})
    except Exception as e:
        logging.error({'today': current_date,
                                                                 'levelname': 'ERROR',
                                                                 'message': e})
    logging.info({'today': current_date,
                                                            'levelname': 'INFO',
                                                            'message': 'End test_func'})


if __name__ == '__main__':
    a = 1
    test_func(a)
