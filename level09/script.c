#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char transform(char c, size_t i) { return c - i; }

int main(int ac, char **av) {
  int fd = open(av[1], O_RDONLY);
  char line[27];
  int i = read(fd, &line, 26);
  line[i] = 0;
  for (size_t s = 0; line[s] && line[s] != '\n'; ++s) {
    char c = transform(line[s], s);
    write(1, &c, 1);
  }
  write(1, "\n", 1);
}
