
# coding: utf-8

import logging
from lightfm import LightFM
from lightfm.evaluation import auc_score, precision_at_k
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def train_hybrid_recommender(Mui_tr, Mui_if, Mui_uf):
    logger.info('Training hybrid recommender')
    model = LightFM(no_components=30, loss='warp')
    model.fit_partial(
            Mui_tr, item_features = Mui_if, user_features=Mui_uf,
            epochs=30,
            verbose=True)
    logger.info('Returning hybrid recommender model')
    return model

def validate_hybrid_recommender(Mui_tr, Mui_if, Mui_uf):
    logger.info('Validating the recommender')
    train_auc = auc_score(model, Mui_tr, item_features = Mui_if, user_features=Mui_uf).mean()
    train_pre = precision_at_k(model, Mui_tr, item_features = Mui_if, user_features=Mui_uf).mean()
    return(train_auc, train_pre)

