data Result t e = Ok t | Err e

okOr : Maybe t -> e -> Result t e
okOr (Just x) _ = Ok x
okOr Nothing e = Err e

allOk : List (Result t e) -> Result (List t) e
allOk list = foldr glomError (Ok []) list where
  glomError : Result t e -> Result (List t) e -> Result (List t) e
  glomError _ (Err err) = Err err
  glomError (Err err) (Ok list) = Err err
  glomError (Ok elem) (Ok list) = Ok (elem :: list)

(Show t, Show e) => Show (Result t e) where
  show (Ok t) = "Ok " ++ (show t)
  show (Err e) = "Err " ++ (show e)
