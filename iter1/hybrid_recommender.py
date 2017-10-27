
# coding: utf-8

from lightfm import LightFM
from lightfm.evaluation import auc_score, precision_at_k


def train_hybrid_recommender(Mui_tr, Mui_if, Mui_uf):
    model = LightFM(loss='warp',
                    random_state=2016,
                    no_components=59,
                    learning_rate=0.0271016262622,
                    user_alpha=0.000114232541556 * 0.0505980387466,#item_alpha*scale
                    item_alpha=0.000114232541556)
    model.fit_partial(
            Mui_tr,
            epochs=68,
            verbose=True)
    return model

def validate_hybrid_recommender(Mui_tr, Mui_if, Mui_uf):
    train_auc = auc_score(model, Mui_tr, item_features = Mui_if, user_features=Mui_uf).mean()
    train_pre = precision_at_k(model, Mui_tr, item_features = Mui_if, user_features=Mui_uf).mean()
    return(train_auc, train_pre)
