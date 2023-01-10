from ..documents import Article

def create_index():
  Article.init()

if __name__ == '__main__':
  create_index()