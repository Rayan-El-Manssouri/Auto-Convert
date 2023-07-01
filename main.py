from message_terminal.message import color_text_terminal
color_text_terminal("Chargement en cours...", "red", 0.01)
color_text_terminal("Traitement des données du PDF...", "red", 0.01)
import json
import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
pdf_path = config.get("paths", "pdf_path")
json_path = config.get("paths", "json_path")
output_dir = config.get("paths", "output_dir")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


from text.extract import extract_text_coords_font_from_pdf
pdf_data = extract_text_coords_font_from_pdf("example.pdf")
pdf_data_output_file = os.path.join(output_dir, "pdf_data.json")


with open(os.path.join(output_dir, "pdf_data.json"), "w", encoding="utf-8") as f:
    json.dump(pdf_data, f, ensure_ascii=False, indent=4)

from generateReactComponent.reactComponentGenerator import generate_react_component
react_component_path = config.get("paths", "react_component_path")


react_component = generate_react_component(pdf_data)

output_dir = config.get("paths", "output_dir")

config.read("config.ini")
json_path = config.get("paths", "json_path")
react_component_path = config.get("paths", "react_component_path")

react_component = generate_react_component(pdf_data)
custom_view_dir = os.path.join(output_dir, "CustomView")
view_component = """
import React from 'react';
import { Text, View } from '@react-pdf/renderer';
const PdfCustomView = () => {
  // Mettez ici le code de la vue personnalisée pour le PDF
};
export default PdfCustomView;
"""



if not os.path.exists(custom_view_dir):
    os.makedirs(custom_view_dir)

view_component = """
import React from 'react';
import { Text, View } from '@react-pdf/renderer';
const CustomView = ({ color, stateName, left, top, text, fontFamily, fontSize, valeur, LeftText, TopLeft, widthView, heightView }) => {
  const [isChecked, setIsChecked] = React.useState(stateName === valeur);
  const leftValue = LeftText ? LeftText : 12;
  const topValue = TopLeft ? TopLeft : 0;
  const width = widthView ? widthView : 10;
  const height = heightView ? heightView : 10;

  React.useEffect(() => {
    setIsChecked(valeur ? stateName === valeur : text === stateName);
  }, [stateName, valeur, text]);

  return (
    <View
      style={{
        width: width,
        height: height,
        borderWidth: 1,
        borderColor: color,
        marginLeft: 5,
        backgroundColor: '#fff',
        position: 'absolute',
        left: left,
        top: top,
      }}
    >
      {isChecked ? (
        <Text
          style={{
            flex: 1,
            fontSize: 10,
            fontWeight: 'bold',
            position: 'absolute',
            textAlign: 'center',
            left: '0.5',
            top: '-1.5',
          }}
        >
          X
        </Text>
      ) : (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
          <View style={{ width: '60%', height: 2, backgroundColor: 'transparent' }} />
        </View>
      )}
      {text && (
        <Text
          style={{
            position: 'absolute',
            left: leftValue,
            top: topValue,
            fontSize: fontSize,
            width: 500,
            color: color,
            fontFamily: fontFamily,
          }}
        >
          {text}
        </Text>
      )}
    </View>
  );
};

export default CustomView;
"""

with open(os.path.join(custom_view_dir, "CustomView.js"), "w", encoding="utf-8") as f:
    f.write(view_component)

with open(os.path.join(output_dir, "react_component.js"), "w", encoding="utf-8") as f:
    f.write(react_component)

color_text_terminal("Chargement terminé !", "green", 0.01)
