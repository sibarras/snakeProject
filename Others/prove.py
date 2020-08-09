import curses

def get_param(screen, prompt_string):
     curses.echo()
     screen.clear()
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(2, len(prompt_string)+2, 60)
     return input

def sumar(screen):
    curses.noecho()
    n = int(get_param(screen, 'Ingrese un número: '))
    m = int(get_param(screen, 'Ingrese otro número: '))
    screen.addstr(2, 2, 'La suma de {} y {} es {}.'.format(n, m, n + m))
    screen.addstr(4, 2, 'Pulse Enter para volver al menú')
    while True:
        ch = screen.getch()
        if ch == 10: #Enter
            main(screen)
            break

def restar(screen):
    curses.echo()
    n = int(get_param(screen, 'Ingrese un número: '))
    m = int(get_param(screen, 'Ingrese otro número: '))
    screen.addstr(2, 2, 'La resta de {} y {} es {}.'.format(n, m, n - m))
    screen.addstr(4, 2, 'Pulse Enter para volver al menú')
    while True:
        ch = screen.getch()
        if ch == 10: #Enter
            main(screen)
            break


def main(screen):
    curses.echo()
    while True:
        screen.clear()
        screen.border(0)
        screen.addstr(2, 2, "Alt+A para sumar dos numeros")
        screen.addstr(3, 2, "Alt+P para restar dos numeros")
        screen.addstr(4, 2, "Alt+E para salir de la app")
        ch = screen.getch(5, 2)

        if ch == 27: #Tecla Alt
            screen.nodelay(True)
            ch2 = screen.getch() # obtener tecla pulsada despues de Alt
            if ch2 == -1 or ch2 == ord('e') or ch2 == ord('E'):
                break
            elif ch2 == ord('a') or ch2 == ord('A'):
                screen.nodelay(False)
                sumar(screen)
                break
            elif ch2 == ord('p') or ch2 == ord('P'):
                screen.nodelay(False)
                restar(screen)
                break
            else:
                screen.refresh()
            screen.nodelay(False)


curses.wrapper(main)