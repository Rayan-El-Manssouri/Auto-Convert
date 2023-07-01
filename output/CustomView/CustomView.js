
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
