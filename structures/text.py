__all__ = ["Text"]


class TextPart:
    quoted_key = True
    do_camel_case = False

    def __init__(self,
                 text: str,
                 color: str | None = None,
                 bold: bool = None,
                 italic: bool = False,
                 underlined: bool = None,
                 strikethrough: bool = None,
                 obfuscated: bool = None) -> None:
        self.text = text
        self.color = color
        self.bold = bold
        self.italic = italic
        self.underlined = underlined
        self.strikethrough = strikethrough
        self.obfuscated = obfuscated
    
    def __str__(self) -> str:
        additions = []

        for k, v in self.__dict__.items():
            if v is None:
                continue
            elif isinstance(v, bool):
                additions.append(f'"{k}":"{str(v).lower()}"')
            else:
                additions.append(f'"{k}":"{v}"')
        
        res = ",".join(additions)
        return f"{{{res}}}"

    def __repr__(self) -> str:
        return self.__str__()


class Text:
    def __init__(self, text: str, markup: bool = True) -> None:
        self.raw = text
        self.markup = markup
        self.parts = []
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        if self.markup:
            if '\n' in self.raw:
                texts = list(map(Text, self.raw.split("\n")))
                return str(texts)
            cur = {"color": None, "bold": None, "italic": False, "underlined": None, "strikethrough": None, "obfuscated": None}
            buf = ""
            spec = ""
            proc_spec = 0
            parts = []

            for c in self.raw:
                if not proc_spec:
                    if c == "[":
                        proc_spec = 1
                        if buf:
                            parts.append(TextPart(buf, **cur))
                        buf = ""
                    elif c == "&":
                        proc_spec = 2
                    else:
                        buf += c
                elif proc_spec == 1: # processing opened tag with "["
                    if c == "]":
                        match spec:
                            case "b":
                                cur["bold"] = True
                                spec = ""
                                proc_spec = 0
                            case "/b":
                                cur["bold"] = None
                                spec = ""
                                proc_spec = 0
                            case "i":
                                cur["italic"] = True
                                spec = ""
                                proc_spec = 0
                            case "/i":
                                cur["italic"] = False
                                spec = ""
                                proc_spec = 0
                            case "u":
                                cur["underlined"] = True
                                spec = ""
                                proc_spec = 0
                            case "/u":
                                cur["underlined"] = None
                                spec = ""
                                proc_spec = 0
                            case "s":
                                cur["strikethrough"] = True
                                spec = ""
                                proc_spec = 0
                            case "/s":
                                cur["strikethrough"] = None
                                spec = ""
                                proc_spec = 0
                            case "o":
                                cur["obfuscated"] = True
                                spec = ""
                                proc_spec = 0
                            case "/o":
                                cur["obfuscated"] = None
                                spec = ""
                                proc_spec = 0
                            case "/color":
                                cur["color"] = None
                                spec = ""
                                proc_spec = 0
                            case s if "color" in s:
                                try:
                                    col = s.split('=')[1]
                                except IndexError:
                                    raise SyntaxError("You should write color tag as [color=<color>]")
                                cur["color"] = col
                                spec = ""
                                proc_spec = 0   
                    else:
                        spec += c
                else:
                    spec += c
                    match spec:
                        case "lb":
                            buf += "["
                            spec = ""
                            proc_spec = 0
                        case "rb":
                            buf += "]"
                            spec = ""
                            proc_spec = 0
                        case "amp":
                            buf += "&"
                            spec = ""
                            proc_spec = 0
            
            if buf:
                parts.append(TextPart(buf, **cur))
            
            if len(parts) == 1:
                return f"'{str(parts[0])}'"
            return f"'{str(parts)}'"
        else:
            return self.raw

