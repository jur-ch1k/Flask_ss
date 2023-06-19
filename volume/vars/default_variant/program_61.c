for(i = 2; i <= n+1; ++i)
   C[i] = C[i - 1] + D[i];
for(i = 2; i <= n+1; ++i)
   for(j = 2; j <= m+1; ++j)
      B[i][j] = B[i - 1][j + 1] + C[n + 1];
for(i = 2; i <= n+1; ++i){
   A[i][1][1]= C[i];
   for(j = 2; j <= m+1; ++j){
      for(k = 1; k <= n; ++k)
         A[i][j][k] = A[i][j - 1][k - 1] + A[i][j][k];
}