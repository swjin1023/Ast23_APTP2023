import UI
import variables
global main_page

if __name__ == "__main__":
    main_page = UI.StartUI(variables.root)
    variables.root.mainloop()
