from sklearn.feature_extraction.text import CountVectorizer
from scipy import sparse

vec = CountVectorizer(token_pattern=r"[a-z']{3,}", min_df=30, binary=True)
X = vec.fit_transform(df["tl"])                        # bài × từ (có hoặc không)
vocab = np.array(vec.get_feature_names_out())

ngay0 = df["t"].dt.normalize().min()
day_idx = (df["t"].dt.normalize() - ngay0).dt.days.values
D = sparse.csr_matrix((np.ones(len(df)), (np.arange(len(df)), day_idx)))
C = (X.T @ D).toarray()                                # từ × ngày: số bài chứa từ
N = np.bincount(day_idx)                               # số bài mỗi ngày


def top_words(ngay, k=10, toi_thieu=300):
    """Từ nổi bật nhất của một ngày so với TẤT CẢ các ngày trước đó."""
    i = (pd.Timestamp(ngay) - ngay0).days
    truoc = C[:, :i].sum(1) / N[:i].sum()               # tần suất trước ngày đó
    lift = (C[:, i] / N[i]) / (truoc + 1 / N.sum())
    lift[C[:, i] < toi_thieu] = 0                       # bỏ từ quá hiếm (lỗi chính tả)
    best = np.argsort(-lift)[:k]
    return [(vocab[j], int(C[j, i]), round(float(lift[j]))) for j in best]


for ngay in ["2011-05-18", "2011-05-19", "2011-05-20"]:
    print(ngay[5:], [f"{w} ({lift}x)" for w, c, lift in top_words(ngay)])
